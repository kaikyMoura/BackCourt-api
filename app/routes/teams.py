from typing import List, Optional
from fastapi import APIRouter, FastAPI, Query
from app.services.nba_api.nba_client import get_all_teams, get_team_by_name, get_team_by_nickname

app = FastAPI()
router = APIRouter()

@router.get("/teams", response_model=List[dict])
def get_teams(
        nickname: Optional[str] = Query(None, description="Filter by team nickname"), 
        name: Optional[str] = Query(None, description="Filter by team name"),
        limit: Optional[int] = Query(None, description="Limit the number of teams"),
        page: Optional[int] = Query(None, description="Paginate the teams"),
        pageSize: Optional[int] = Query(10, description="Paginate the teams")
    ):
    teams = []
    
    if nickname:
        teams = list(filter(lambda team: teams.lower() in team["nickname"].lower(), get_team_by_nickname))
     
    if name:
        teams = list(filter(lambda team: teams.lower() in team["full_name"].lower(), get_team_by_name))
        
    else:
        teams = get_all_teams()
    
    if limit:
        teams = teams[:limit]
        
    if page:
        page = page or 1
        teams = teams[(page-1) * pageSize: page * pageSize]
        
    return teams