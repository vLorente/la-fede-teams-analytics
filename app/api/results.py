"""Fast API Endpoints"""
from fastapi import APIRouter

PREFIX = '/results'
router = APIRouter()

@router.get("/results")
def hello_world():
    return 'Hello World'
