"""Selectores genéricos para el modelo Result"""

from sqlalchemy.orm import Session
from app.models import Result


def search_results(session: Session, filters=None, limit=None):
    """
    Realiza una búsqueda de resultados basada en filtros proporcionados.

    Args:
        session (Session): Objeto de sesión SQLAlchemy.
        filters (dict): Diccionario de filtros donde las claves son los
        nombres de las columnas y los valores son los valores de filtrado.
        limit (int): Limite de registros devueltos por la consulta.

    Returns:
        List[Result]: Lista de resultados que coinciden con los filtros.
    """
    query = session.query(Result)

    if filters:
        for key, value in filters.items():
            if hasattr(Result, key):
                query = query.filter(getattr(Result, key) == value)

    if limit:
        limit = int(limit)
        query.limit(limit)

    results = query.all()
    return results
