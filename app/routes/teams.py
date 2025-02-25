from typing import List, Optional
from fastapi import APIRouter, FastAPI, Query
from app.services.nba_api.nba_client import get_all_teams, get_team_by_name

app = FastAPI()
router = APIRouter()

@router.get("/teams", response_model=List[dict])
def get_teams(
        name: Optional[str] = Query(None, description="Filter by team name"),
        limit: Optional[int] = Query(None, description="Limit the number of teams"),
        page: Optional[int] = Query(None, description="Paginate the teams"),
        pageSize: Optional[int] = Query(None, description="Paginate the teams")
    ):
    teams = []
     
    if name:
        teams = [team for team in get_team_by_name(name) if name.lower() in team["full_name"].lower()]
        
    else:
        teams = get_all_teams()
    
    if limit:
        teams = teams[:limit]
        
    if page:
        teams = teams[(page-1)*pageSize:page*pageSize]
        
    return teams