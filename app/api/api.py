from fastapi import APIRouter
from app.api.routers import teams, results

api_router = APIRouter()

api_router.include_router(results.router, prefix="/results", tags=["results"])
api_router.include_router(teams.router, prefix="/teams", tags=["teams"])
