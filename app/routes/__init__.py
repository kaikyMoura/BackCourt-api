from .players_route import router as players_route
from .teams_route import router as teams_route
from .articles_route import router as articles_route
from fastapi import APIRouter

router = APIRouter()


router.include_router(players_route)
router.include_router(articles_route)
router.include_router(teams_route)