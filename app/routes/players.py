from collections import defaultdict
from typing import List, Optional

from fastapi.responses import JSONResponse
import pandas as pd
from app.services.nba_api.nba_client import (
    get_active_players,
    get_all_players,
    get_player_awards,
    get_player_carrer_totals,
    get_player_info,
    get_inactive_players,
)
from fastapi import APIRouter, FastAPI, HTTPException, Query

app = FastAPI()
router = APIRouter()


@router.get("/players", response_model=List[dict])
def get_players(
    is_active: Optional[bool] = Query(None, description="Filter by active players"),
    player_name: Optional[str] = Query(None, description="Filter by player name"),
    limit: Optional[int] = Query(None, description="Limit the number of players"),
    page: Optional[int] = Query(None, description="Paginate the teams"),
    pageSize: Optional[int] = Query(10, description="Paginate the teams"),
):

    players = []

    if is_active is True:
        players = get_active_players()
    elif is_active is False:
        players = get_inactive_players()
    else:
        players = get_all_players()

    if player_name:
        players = list(
            filter(lambda p: player_name.lower() in p["full_name"].lower(), players)
        )

    if limit:
        players = players[:limit]

    if page:
        page = page or 1
        players = players[(page - 1) * pageSize : page * pageSize]

    return JSONResponse(content=players)


@router.get("/players/carrer_stats/totals/{player_id}", response_model=dict)
def get_player_carrer_totals_by_id(
    player_id: str,
    regular_season: Optional[bool] = Query(
        True, description="Filter by regular season stats"
    ),
    post_season: Optional[bool] = Query(False, description="Filter by playoffs stats"),
    season: Optional[str] = Query(
        None, description="Filter by specific season, e.g., '2023-24'"
    ),
    page: Optional[int] = Query(None, description="Paginate the seasons"),
    pageSize: Optional[int] = Query(10, description="Paginate the seasons"),
):
    if not player_id:
        raise HTTPException(
            status_code=401,
            detail="Param player_id is required",
        )

    player = get_player_carrer_totals(player_id)

    if regular_season:
        df = player.season_totals_regular_season.get_data_frame()
    elif post_season:
        df = player.season_totals_post_season.get_data_frame()
    else:
        df = player.career_totals_regular_season.get_data_frame()

    if season:
        df = df[df["SEASON_ID"] == season]

        if df.empty:
            raise HTTPException(
                status_code=404,
                detail="No season stats found for this player in season {season}",
            )

    # Check if the player has played any games
    if "GP" not in df.columns or df["GP"].sum() == 0:
        return df

    stats = [
        "PTS",
        "REB",
        "AST",
        "STL",
        "BLK",
        "TOV",
        "FGM",
        "FGA",
        "FG3M",
        "FG3A",
        "FTM",
        "FTA",
    ]

    # Calculate per game stats
    for stat in stats:
        if stat in df.columns:
            per_game_col = f"{stat}_PER_GAME"
            df[per_game_col] = (df[stat] / df["GP"]).round(1)

    df.columns = df.columns.str.lower()

    if page:
        start = (page - 1) * pageSize
        end = start + pageSize
        result = result[start:end]

    return JSONResponse(content=df.to_dict(orient="records"))


# Retrieve general information about the player (age, height, weight, etc.)
@router.get("/players/player/info", response_model=dict)
def get_player_common_info(
    player_id: Optional[int] = Query(None, description="Filter by player id"),
    player_name: Optional[str] = Query(None, description="Filter by player name"),
):

    if not player_id and not player_name:
        raise HTTPException(
            status_code=400, detail="Either player_id or player_name must be provided"
        )

    if player_id:
        player_info = get_player_info(player_id)
        return {"player_id": player_id, "player_info": player_info}

    if player_name:
        all_players = get_all_players()
        filtered_players = list(
            filter(lambda p: player_name.lower() in p["full_name"].lower(), all_players)
        )

        if not filtered_players:
            raise HTTPException(
                status_code=404, detail="No players found with that name"
            )

        player_infos = [get_player_info(player["id"]) for player in filtered_players]

        df = pd.DataFrame(player_infos)
        df.columns = df.columns.str.lower()

        return JSONResponse(content=df.to_dict(orient="records"))


@router.get("/players/player/awards", response_model=dict)
def fetch_player_awards(
    player_id: int = Query(None, description="Filter by player id"),
    detailed: Optional[bool] = Query(
        False, description="Return detailed awards information"
    ),
):
    """
    Fetches awards for a specific player by their player ID.

    Args:
        player_id (int): The unique identifier for the player.
        detailed (bool, optional): If True, returns detailed awards information including descriptions. Defaults to False.

    Returns:
        dict: A dictionary containing either a summary string of awards or detailed awards information.
            - If detailed is False, returns a summary string of awards.
            - If detailed is True, returns a dictionary with 'summary' and 'details' keys.

    Raises:
        HTTPException: If player_id is not provided or if no awards are found for the player.
    """

    if not player_id:
        raise HTTPException(
            status_code=400, detail="Missing required parameter: player_id"
        )

    raw_awards = get_player_awards(player_id)

    if not raw_awards:
        return {"summary": "", "details": []} if detailed else ""

    award_counts = defaultdict(int)

    processed_awards = []
    
    for award in raw_awards:
            description = award.get('description', '')
            
            if "All-Defensive" in description:
                award_type = "All-Defensive Team"
            elif "All-Star" in description:
                award_type = "NBA All-Star"
            elif "Player of the Week" in description:
                award_type = "NBA Player of the Week"
            elif "Gold Medal" in description:
                award_type = "Olympic Gold Medal"
            else:
                award_type = description
            
            award_counts[award_type] += 1
            
            processed_awards.append(award)

    summary = " | ".join([
        f"{count} {award}" 
        for award, count in sorted(
            award_counts.items(),
            key=lambda x: (-x[1], x[0]))
    ])

    if not detailed:
        return JSONResponse(content=summary)

    return {"summary": summary, "details": raw_awards}
