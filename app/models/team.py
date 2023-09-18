"""Sql Alchemy Model Team"""
from sqlalchemy import Column, Integer, String
from app.database import Base

class Team(Base):
    """Modelo Tabla Teams"""

    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    season = Column(String)
    team = Column(String)
    location = Column(String)
    color_home = Column(String)
    color_visitor = Column(String)
