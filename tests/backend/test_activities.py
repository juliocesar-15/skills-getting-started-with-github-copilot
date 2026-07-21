from fastapi.testclient import TestClient

from src import app as app_module


def test_root_redirect():
    client = TestClient(app_module.app)
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (301, 302, 303, 307, 308)
    assert "/static/index.html" in response.headers.get("location", "")


def test_get_activities():
    client = TestClient(app_module.app)
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    client = TestClient(app_module.app)
    email = "tester@mergington.edu"

    # Signup
    resp = client.post("/activities/Chess%20Club/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in app_module.activities["Chess Club"]["participants"]

    # Duplicate signup should be rejected
    resp2 = client.post("/activities/Chess%20Club/signup", params={"email": email})
    assert resp2.status_code == 409

    # Unregister
    resp3 = client.delete("/activities/Chess%20Club/signup", params={"email": email})
    assert resp3.status_code == 200
    assert email not in app_module.activities["Chess Club"]["participants"]


def test_signup_activity_not_found():
    client = TestClient(app_module.app)
    resp = client.post("/activities/Nonexistent/signup", params={"email": "a@a.com"})
    assert resp.status_code == 404


def test_unregister_not_signed_up():
    client = TestClient(app_module.app)
    resp = client.delete("/activities/Chess%20Club/signup", params={"email": "not@there.com"})
    assert resp.status_code == 404
