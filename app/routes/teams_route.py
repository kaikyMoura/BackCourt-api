from typing import List, Optional
from fastapi import APIRouter, FastAPI, Query
from fastapi.responses import JSONResponse
from app.services.nba_api.nba_client_service import get_all_teams, get_team_by_name, get_team_by_nickname

app = FastAPI()
router = APIRouter()

@router.get("/teams", response_model=List[dict])
def get_teams(
        nickname: Optional[str] = Query(None, description="Filter by team nickname"), 
        name: Optional[str] = Query(None, description="Filter by team name"),
        limit: Optional[int] = Query(None, description="Limit the number of teams"),
        page: Optional[int] = Query(None, description="Paginate the teams"),
        page_size: Optional[int] = Query(10, description="Paginate the teams")
    ):
    teams = []
    
    if nickname:
        teams = list(filter(lambda team: nickname.lower() in team["nickname"].lower(), get_team_by_nickname(nickname)))
     
    if name:
        teams = list(filter(lambda team: name.lower() in team["full_name"].lower(), get_team_by_name(name)))
        
    else:
        teams = get_all_teams()
    
    if limit:
        teams = teams[:limit]
        
    if page:
        page = page or 1
        if page_size is not None:
            teams = teams[(page - 1) * page_size : page * page_size]
        
    return JSONResponse(content=teams)