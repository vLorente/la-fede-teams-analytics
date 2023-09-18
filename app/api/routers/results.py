"""Fast API Results Endpoints"""
from fastapi import APIRouter
from app.database import SessionLocal
from app.crud.results import search_results

router = APIRouter()
session = SessionLocal()

@router.get('')
async def get_results():
    result = search_results(session)
    return result

@router.get('/team/{team}')
async def get_team(team: str):
    filters = {
        'team': team,
    }
    result = search_results(session, filters=filters)
    return result

@router.get('/season/{season}')
async def get_season(season: str):
    filters = {
        'season': season,
    }
    result = search_results(session, filters=filters)
    return result
