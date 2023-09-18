from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.database import Base, test_engine, SessionTest

client = TestClient(app)

# Cliente de pruebas para interactuar con la API
def get_test_session() -> Session:
    # Pre limpieza de la base de datos

    Base.metadata.create_all(bind=test_engine)
    return SessionTest()
