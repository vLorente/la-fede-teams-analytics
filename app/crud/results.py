"""Selectores genéricos para el modelo Result"""

from sqlalchemy.orm import Session
from app.models.result import Result


def search_results(db: Session, filters=None, limit=None):
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
    query = db.query(Result)

    if filters:
        for key, value in filters.items():
            if hasattr(Result, key):
                query = query.filter(getattr(Result, key) == value)

    if limit:
        limit = int(limit)
        query.limit(limit)

    results = query.all()
    return results

def create_result(db: Session, result: Result):
    """Crea nuevo result

    Args:
        db (Session): conexión con base de datos
        result (Result): Nuevo Result
    """
    db_result = Result(
        season=result.season,
        team=result.team,
        phase=result.phase,
        group=result.group,
        position=result.position,
        matches_played=result.matches_played,
        win=result.win,
        lose=result.lose,
        scored=result.scored,
        against=result.against,
        points=result.points
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result
