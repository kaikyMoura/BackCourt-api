from typing import List, Optional
from app.services.scrapper import get_articles
from fastapi import APIRouter, FastAPI, Query

app = FastAPI()
router = APIRouter()

@router.get("/articles", response_model=List[dict])
def get_nba_articles(
    source: Optional[str] = Query(None, description="Filter by source"),
    player: Optional[str] = Query(None, description="Filter by player name"),
    limit: Optional[int] = Query(None, description="Limit the number of articles"),
):
    articles = get_articles()
    
    if source:
        articles = [a for a in articles if a["source"].lower() == source.lower()]

    if limit:
        articles = articles[:limit]
        
    if player:
        articles = [a for a in articles if player.lower() in a["title"].lower()]

    return articles