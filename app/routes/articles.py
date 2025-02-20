from typing import List, Optional
from app.services.scrapper import get_articles
from fastapi import APIRouter, FastAPI, Query

app = FastAPI()
router = APIRouter()

@router.get("/articles", response_model=List[dict])
def get_nba_articles(
    source: Optional[str] = Query(None, description="Filter by source"),
    player: Optional[str] = Query(None, description="Filter by player name"),
    team: Optional[str] = Query(None, description="Filter by team name"),
    limit: Optional[int] = Query(None, description="Limit the number of articles"),
):
    articles = get_articles()
    
    if source:
        articles = [a for a in articles if a["source"].lower() == source.lower()]

    if limit:
        articles = articles[:limit]
        
    if player:
         for article in articles :
                if player.lower() in article["title"].lower() or player.lower() in article["url"].lower():
                    return [article]
                
    if team:
         for article in articles :
                if team.lower() in article["title"].lower() or team.lower() in article["url"].lower():
                    return [article]
        

    return articles