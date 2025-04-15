from typing import List, Optional

from fastapi.responses import JSONResponse
from app.services.scrapper import get_articles
from fastapi import APIRouter, FastAPI, Query

app = FastAPI()
router = APIRouter()


@router.get("/articles", response_model=List[dict])
def get_nba_articles(
    source: Optional[str] = Query(None, description="Filter by source"),
    player_name: Optional[str] = Query(None, description="Filter by player name"),
    team_name: Optional[str] = Query(None, description="Filter by team name"),
    limit: Optional[int] = Query(None, description="Limit the number of articles"),
    page: Optional[int] = Query(None, description="Paginate the articles"),
    pageSize: Optional[int] = Query(10, description="Paginate the articles"),
):
    articles = get_articles()

    if source is None:
        articles = sorted(articles, key=lambda x: x["source"].lower() != "nba")
    else:
        articles = [a for a in articles if a["source"].lower() == source.lower()]

    if limit:
        articles = articles[:limit]

    if player_name:
        name_parts = player_name.lower().split()
        filtered_articles = [
            article for article in articles
            if any(part in article["title"].lower() or part in article["url"].lower() for part in name_parts)
        ]
        return filtered_articles

    if team_name:
        for article in articles:
            if (
                team_name.lower() in article["title"].lower()
                or team_name.lower() in article["url"].lower()
            ):
                return [article]

    if page:
        page = page or 1
        articles = articles[(page - 1) * pageSize : page * pageSize]

    return JSONResponse(content=articles)
