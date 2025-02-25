from typing import List, Optional
from app.services.nba_api.nba_client import get_active_players, get_all_players, get_player_carrer_stats
from fastapi import APIRouter, FastAPI, Query

app = FastAPI()
router = APIRouter()

@router.get("/players", response_model=List[dict])
def get_players(
    is_active: Optional[bool] = Query(True, description="Filter by active players"),
    player: Optional[str] = Query(None, description="Filter by player name"),
    limit: Optional[int] = Query(None, description="Limit the number of articles"),
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
    
    return players


@router.get("/players/carrer_stats/totals/{player_id}", response_model=dict)
def get_carrer_stats_by_player_id(player_id,
                                  regular_season: Optional[bool] = Query(True, description="Filter by regular season stats"),
                                  post_season: Optional[bool] = Query(False, description="Filter by playoffs stats")):
    
    player = get_player_carrer_stats(player_id)
    
    if regular_season:
        player = player.career_totals_regular_season.get_dict()
    
    if post_season:
        player = player.career_totals_post_season.get_dict()
    
    if not regular_season and not post_season:
        player = player.get_dict().get("resultSets")[0]
    
    return player