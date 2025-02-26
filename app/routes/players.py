from typing import List, Optional
from app.services.nba_api.nba_client import get_active_players, get_all_players, get_player_carrer_stats, get_player_info
from fastapi import APIRouter, FastAPI, Query

app = FastAPI()
router = APIRouter()

@router.get("/players", response_model=List[dict])
def get_players(
    is_active: Optional[bool] = Query(True, description="Filter by active players"),
    player: Optional[str] = Query(None, description="Filter by player name"),
    limit: Optional[int] = Query(None, description="Limit the number of players"),
    page: Optional[int] = Query(None, description="Paginate the teams"),
    pageSize: Optional[int] = Query(10, description="Paginate the teams")
):
    
    players = []
    
    if is_active:
        active_players = get_active_players()
        players = active_players
        
    if not is_active:
        players = get_all_players()  
    
    if player:
        players = list(filter(lambda p: player.lower() in p["full_name"].lower(), players))
    if limit:
        players = players[:limit]
    
    if page:
        players = players[(page-1)*pageSize:page*pageSize]
    
    return players


@router.get("/players/carrer_stats/totals/{player_id}", response_model=dict)
def get_carrer_stats_by_player_id(player_id,
                                  regular_season: Optional[bool] = Query(True, description="Filter by regular season stats"),
                                  post_season: Optional[bool] = Query(False, description="Filter by playoffs stats"),
                                  page: Optional[int] = Query(None, description="Paginate the players"),
                                pageSize: Optional[int] = Query(10, description="Paginate the players")):
    
    player = get_player_carrer_stats(player_id)
    
    if regular_season:
        player = player.career_totals_regular_season.get_dict()
    
    if post_season:
        player = player.career_totals_post_season.get_dict()
    
    if not regular_season and not post_season:
        player = player.get_dict().get("resultSets")[0]
    
    if page:
        player = player[(page-1)*pageSize:page*pageSize]
    
    return player


@router.get('/players/player/info', response_model=dict)
def get_info(player_name: str = Query(None, description="Filter by player name")):
    
    player_info = []
    
    all_players = get_all_players()
    filtered_players = list(filter(lambda p: player_name.lower() in p["full_name"].lower(), all_players))
    for player in filtered_players:
        player_info.append(get_player_info(player["id"]))
    
    return {player_info}