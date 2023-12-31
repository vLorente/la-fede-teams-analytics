"""Selectores genéricos para el modelo Team"""

from sqlalchemy.orm import Session
from app.models.team import Team


def search_teams(db: Session, filters=None, limit=None):
    """
    Realiza una búsqueda de resultados basada en filtros proporcionados.

    Args:
        session (Session): Objeto de sesión SQLAlchemy.
        filters (dict): Diccionario de filtros donde las claves son los
        nombres de las columnas y los valores son los valores de filtrado.
        limit (int): Limite de registros devueltos por la consulta.

    Returns:
        List[Team]: Lista de resultados que coinciden con los filtros.
    """
    query = db.query(Team)

    if filters:
        for key, value in filters.items():
            if hasattr(Team, key):
                query = query.filter(getattr(Team, key) == value)
    if limit:
        limit = int(limit)
        query.limit(limit)

    results = query.all()
    return results

def create_team(db: Session, team: Team):
    """Crea nuevo Team

    Args:
        db (Session): conexión con base de datos
        team (Team): nuevo Team
    """
    db_team = Team(
        team=team.team,
        location=team.location,
        color_home=team.color_home,
        color_visitor=team.color_visitor
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team
