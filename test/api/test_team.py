from test.utils import client, get_test_session
from app.models.team import Team
from app.crud.teams import create_team

# Prueba para GET /
def test_get_teams():
    response = client.get("/teams")
    assert response.status_code == 200
    assert len(response.json()) > 0

# Prueba para GET /team/{team}
def test_get_team():
    # Crear un equipo ficticio para la prueba
    db = get_test_session()
    fake_team = Team(
        team="Fake Team",
        location="Fake Location",
        color_home="Red",
        color_visitor="Blue")
    create_team(db, fake_team)

    response = client.get("/teams/team/Fake%20Team")
    assert response.status_code == 200

    db.close()

# Prueba para GET /home/{color}
def test_get_team_by_color_home():
    # Crear un equipo ficticio para la prueba
    db = get_test_session()
    fake_team = Team(
        team="Fake Team 2",
        location="Fake Location 2",
        color_home="Green",
        color_visitor="Yellow")
    create_team(db, fake_team)

    response = client.get("/teams/home/Green")
    assert response.status_code == 200

    db.close()

# Prueba para GET /visitor/{color}
def test_get_team_by_color_visitor():
    # Crear un equipo ficticio para la prueba
    db = get_test_session()
    fake_team = Team(
        team="Fake Team 3",
        location="Fake Location 3",
        color_home="Orange",
        color_visitor="Purple")
    create_team(db, fake_team)

    response = client.get("/teams/visitor/Purple")
    assert response.status_code == 200

    db.close()
