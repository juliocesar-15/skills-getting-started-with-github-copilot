from src import app as app_module


def test_root_redirect(client):
    # Arrange
    # client fixture provided by tests/conftest.py

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (301, 302, 303, 307, 308)
    assert "/static/index.html" in response.headers.get("location", "")


def test_get_activities(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow(client):
    # Arrange
    email = "tester@mergington.edu"

    # Act - signup
    resp = client.post("/activities/Chess%20Club/signup", params={"email": email})

    # Assert - signup succeeded
    assert resp.status_code == 200
    assert email in app_module.activities["Chess Club"]["participants"]

    # Act - duplicate signup
    resp2 = client.post("/activities/Chess%20Club/signup", params={"email": email})

    # Assert - duplicate rejected
    assert resp2.status_code == 409

    # Act - unregister
    resp3 = client.delete("/activities/Chess%20Club/signup", params={"email": email})

    # Assert - unregister succeeded
    assert resp3.status_code == 200
    assert email not in app_module.activities["Chess Club"]["participants"]


def test_signup_activity_not_found(client):
    # Arrange

    # Act
    resp = client.post("/activities/Nonexistent/signup", params={"email": "a@a.com"})

    # Assert
    assert resp.status_code == 404


def test_unregister_not_signed_up(client):
    # Arrange

    # Act
    resp = client.delete("/activities/Chess%20Club/signup", params={"email": "not@there.com"})

    # Assert
    assert resp.status_code == 404
