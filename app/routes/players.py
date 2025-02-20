from typing import List, Optional
from app.services.nba_api.nba_client import get_active_players
from fastapi import APIRouter, FastAPI, Query

app = FastAPI()
router = APIRouter()

@router.get("/players", response_model=List[dict])
def get_players(
    source: Optional[str] = Query(None, description="Filter by source"),
    player: Optional[str] = Query(None, description="Filter by player name"),
    limit: Optional[int] = Query(None, description="Limit the number of articles"),
):
    
    active_players = get_active_players()
    

    if limit:
        articles = active_players[:limit]
    
    return active_players