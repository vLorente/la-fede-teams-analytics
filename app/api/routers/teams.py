"""Fast API Results Endpoints"""
from fastapi import APIRouter
from app.database import SessionLocal
from app.crud.teams import search_teams

router = APIRouter()
session = SessionLocal()

@router.get('')
async def get_teams():
    result = search_teams(session)
    return result

@router.get('/team/{team}')
async def get_team(team: str):
    filters = {
        'team': team.strip(),
    }
    result = search_teams(session, filters=filters)
    return result

@router.get('/home/{color}')
async def get_team_by_color_home(color: str):
    filters = {
        'color_home': color.strip()
    }
    result = search_teams(session, filters=filters)
    return result

@router.get('/visitor/{color}')
async def get_team_by_color_visitor(color: str):
    filters = {
        'color_visitor': color.strip()
    }
    result = search_teams(session, filters=filters)
    return result