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

def test_chat_requires_login(client):
    response = client.get("/chat")
    assert response.status_code == 302  # redirects to login

def test_chat_post_message(client):
    login(client)
    response = client.post("/chat", data={"message": "Recommend a book"}, follow_redirects=True)
    assert response.status_code == 200
    # AI response may vary, just check page renders
    assert b"AI librarian" in response.data or b"Please enter a message" not in response.data
