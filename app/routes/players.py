from collections import defaultdict
from typing import List, Literal, Optional

from fastapi.responses import JSONResponse
import pandas as pd
from app.services.nba_api.nba_client import (
    get_active_players,
    get_all_players,
    get_player_awards,
    get_player_carrer_totals,
    get_player_fantasy_profile,
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


@router.get("/players/stats/carrer/{player_id}", response_model=dict)
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
        description = award.get("description", "")

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

    summary = " | ".join(
        [
            f"{count} {award}"
            for award, count in sorted(
                award_counts.items(), key=lambda x: (-x[1], x[0])
            )
        ]
    )

    if not detailed:
        return JSONResponse(content=summary)

    return {"summary": summary, "details": raw_awards}


@router.get("/players/stats/advanced/{player_id}", response_model=dict)
def get_player_advanced_stats(
    player_id: int,
    dataset: Literal[
        "Overall", "LastNGames", "DaysRestModified", "Opponent"
    ],
    per_mode: Literal["Totals", "Per36", "PerGame"] = "Totals",
    season: Optional[str] = Query(None, description="Filter by season: (2022-23)"),
    season_type: Literal["Regular Season", "Pre Season", "Playoffs"] = "Regular Season",
):

    """
    Retrieve advanced statistics for a specific player.

    Args:
        player_id (int): The unique identifier for the player.
        dataset (Literal): The dataset type to retrieve, options include 
            "Overall", "LastNGames", "DaysRestModified", "Opponent".
        per_mode (Literal): The mode for statistics calculation, options include 
            "Totals", "Per36", "PerGame". Defaults to "Totals".
        season (Optional[str]): The season to filter by, e.g., "2022-23".
        season_type (Literal): The type of season to filter by, options include 
            "Regular Season", "Pre Season", "Playoffs". Defaults to "Regular Season".

    Returns:
        JSONResponse: A JSON response containing the player's advanced statistics 
            based on the specified parameters. If no data is found or if the player 
            has not played any games, an appropriate HTTPException is raised.
    """

    params = {
        "player_id": player_id,
    }

    if per_mode:
        params["per_mode36"] = per_mode
    if season:
        params["season"] = season
    if season_type:
        params["season_type_playoffs"] = season_type

    dataset_index = {
        "Overall": 0,
        "LastNGames": 1,
        "DaysRestModified": 2,
        "Opponent": 3,
    }

    fantasy_profile_df  = get_player_fantasy_profile(params)

    # Check if dataset is valid
    if dataset not in dataset_index:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid parameter dataset: {dataset}.. Available options: {list(dataset_index.keys())}",
        )

    # Get the selected dataset replacing "get_data_frames()[0]"
    df = fantasy_profile_df[dataset_index[dataset]]

    if df.empty:
        raise HTTPException(
            status_code=404, detail="No data found for this player"
        )
    
    df.columns = df.columns.str.lower()

    # Check if the player has played any games
    if "gp" not in df.columns or df["gp"].sum() == 0:
        return JSONResponse(
            content={
                "player_id": player_id,
                "dataset": dataset,
                "per_mode": per_mode or "All",
                "season": season or "All",
                "season_type": season_type or "All",
                "stats": []
            }
        )
    
    stats = [
        "pts", "reb", "ast", "stl", "blk", "tov", "fgm", "fga",
        "fg3m", "fg3a", "ftm", "fta", "dreb", "oreb", "pf", "plus_minus", "min"
    ]

    for stat in stats:
        if stat in df.columns:
            per_game_col = f"{stat}_per_game"
            df[per_game_col] = (df[stat] / df["gp"]).round(1)

    return JSONResponse(
        content={
            "player_id": player_id,
            "dataset": dataset,
            "per_mode": per_mode or "All",
            "season": season or "All",
            "season_type": season_type or "All",
            "stats": df.drop(columns=['group_set'], errors='ignore').to_dict(orient="records"),
        }
)
