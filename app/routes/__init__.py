from numpy import outer
from .players import router as playeres_router
from .teams import router as teams_router
from .articles import router as articles_router
from fastapi import APIRouter

router = APIRouter()


router.include_router(playeres_router)
router.include_router(articles_router)
router.include_router(teams_router)