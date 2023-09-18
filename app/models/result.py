"""Sql Alchemy Model Result"""
from sqlalchemy import Column, Integer, String
from app.database import Base

class Result(Base):
    """Modelo Tabla Resutls"""
    
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    season = Column(String)
    phase = Column(String)
    group = Column(String)
    position = Column(Integer)
    team = Column(String)
    matches_played = Column(Integer)
    win = Column(Integer)
    lose = Column(Integer)
    scored = Column(Integer)
    against = Column(Integer)
    points = Column(Integer)
