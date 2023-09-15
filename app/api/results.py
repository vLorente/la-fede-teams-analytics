"""Fast API Endpoints"""
from fastapi import APIRouter
from app.database import SessionLocal
from app.selectors.results import search_results

PREFIX = '/results'
router = APIRouter()
session = SessionLocal()

@router.get(PREFIX)
def get_results():
    results = search_results(session)
    return results
