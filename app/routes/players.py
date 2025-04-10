from typing import List, Optional
from app.services.nba_api.nba_client import (
    get_active_players,
    get_all_players,
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
    player: Optional[str] = Query(None, description="Filter by player name"),
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

    if player:
        players = list(
            filter(lambda p: player.lower() in p["full_name"].lower(), players)
        )

    if limit:
        players = players[:limit]

    if page:
        page = page or 1
        players = players[(page - 1) * pageSize : page * pageSize]

    return players


@router.get("/players/carrer_stats/totals/{player_id}", response_model=dict)
def get_player_carrer_totals_by_id(
    player_id,
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

    if "PTS" in df.columns and "GP" in df.columns and df["GP"].sum() > 0:
        df["PTS_PER_GAME"] = (df["PTS"] / df["GP"]).round(1)

    result = df.to_dict(orient="records")

    if page:
        start = (page - 1) * pageSize
        end = start + pageSize
        result = result[start:end]

    return {"player_id": player_id, "total_seasons": len(result), "seasons": result}


# Retrieve general information about the player (age, height, weight, etc.)
@router.get("/players/player/info", response_model=dict)
def get_player_info(
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
        return {"query": player_name, "results": player_infos}


# @router.get("/players/carrer_stats/cumulative_player_stats", response_model=dict)
# def get_cumulative_player_stats(gameIds: Optional[List[int]] = Query(None, description="Filter by game ids"),
#                                   league_id: Optional[int] = Query(None, description="Filter by league id"),
#                                   player_id: Optional[int] = Query(None, description="Filter by player id"),
#                                   season: Optional[int] = Query(None, description="Filter by season (ex: 2025)"),
#                                   season_type: Optional[str] = Query(None, description="Filter by season (ex: 2025)")
#                                   ):

#     player = get_cumulative_player_stats(gameIds, league_id, player_id, season, season_type)

#     if regular_season:
#         player = player.career_totals_regular_season.get_dict()

#     if post_season:
#         player = player.career_totals_post_season.get_dict()

#     if not regular_season and not post_season:
#         player = player.get_dict().get("resultSets")[0]

#     if page:
#         player = player[(page-1)*pageSize:page*pageSize]

#     return player
