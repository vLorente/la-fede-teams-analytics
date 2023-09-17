"""Modelos SQL Alchemy"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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


class Team(Base):
    """Modelo Tabla Teams"""

    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    season = Column(String)
    team = Column(String)
    location = Column(String)
    color_home = Column(String)
    color_visitor = Column(String)