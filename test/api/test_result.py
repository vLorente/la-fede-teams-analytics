"""Tests Result"""
from app.main import app
from app.models.result import Result
from app.crud.results import create_result
from test.utils import client, get_test_session

# Prueba para GET /
def test_get_results():
    response = client.get("/results")
    assert response.status_code == 200
    assert len(response.json()) > 0

# Prueba para GET /team/{team}
def test_get_result_by_team():
    # Crear un resultado ficticio para la prueba
    db = get_test_session()
    fake_result = Result(
        season="2023",
        team="Test Team",
        phase="Test Phase",
        group="A",
        position=1,
        matches_played=10,
        win=8, lose=2,
        scored=100,
        against=80,
        points=16)
    create_result(db, fake_result)

    response = client.get("/results/team/Test%20Team")
    assert response.status_code == 200

    db.close()

# Prueba para GET /season/{season}
def test_get_result_by_season():
    # Crear un resultado ficticio para la prueba
    db = get_test_session()
    fake_result = Result(
        season="2023",
        team="Test Team 2",
        phase="Test Phase",
        group="A",
        position=2,
        matches_played=10,
        win=7,
        lose=3,
        scored=90,
        against=70,
        points=14)
    create_result(db, fake_result)

    response = client.get("/results/season/2023")
    assert response.status_code == 200

    db.close()
