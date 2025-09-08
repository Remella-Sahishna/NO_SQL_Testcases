import pytest # type: ignore
from chatbot import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

def login(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1

def test_profile_requires_login(client):
    response = client.get("/profile")
    assert response.status_code == 302  # redirects to login

def test_profile_page(client):
    login(client)
    response = client.get("/profile")
    assert response.status_code == 200
    assert b"Your borrowed books" in response.data or b"Library" in response.data

def test_my_collection_page(client):
    login(client)
    response = client.get("/my_collection")
    assert response.status_code == 200
