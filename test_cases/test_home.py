import pytest # type: ignore
from chatbot import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to NoSQL Library" in response.data

def test_signup(client):
    response = client.post("/", data={
        "username": "Alice",
        "email": "alice@example.com",
        "signup": True
    }, follow_redirects=True)
    assert response.status_code == 200
    

def test_login(client):
    # First create user manually or use a fixture
    response = client.post("/", data={
        "user_id": 1,
        "login": True
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome back" in response.data

def test_logout(client):
    client.post("/", data={"user_id": 1, "login": True})
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"successfully logged out" in response.data
