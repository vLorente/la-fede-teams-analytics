"""Selectores genéricos para el modelo Team"""

from sqlalchemy.orm import Session
from app.models import Team


def search_teams(session: Session, filters=None, limit=None):
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
    query = session.query(Team)

    if filters:
        for key, value in filters.items():
            if hasattr(Team, key):
                query = query.filter(getattr(Team, key) == value)

    if limit:
        limit = int(limit)
        query.limit(limit)

    results = query.all()
    return results
