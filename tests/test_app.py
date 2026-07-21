import pytest

from fastapi.testclient import TestClient

from src import app as app_module


def test_prevents_duplicate_signup():
    # Arrange
    client = TestClient(app_module.app)

    # Act
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    # Assert
    assert response.status_code == 409
    assert response.json()["detail"] == "Student is already signed up for this activity"
    assert len(app_module.activities["Chess Club"]["participants"]) == 2


def test_unregisters_participant():
    # Arrange
    client = TestClient(app_module.app)

    # Act
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    # Assert
    assert response.status_code == 200
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]
