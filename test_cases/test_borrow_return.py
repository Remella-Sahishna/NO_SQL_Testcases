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

def test_borrow_book_requires_login(client):
    response = client.get("/borrow")
    assert response.status_code == 302  # redirects to login

def test_return_book_requires_login(client):
    response = client.get("/return")
    assert response.status_code == 302  # redirects to login

def test_borrow_and_return_flow(client):
    login(client)
    # Borrow book
    response = client.post("/borrow", data={"book_id": 1}, follow_redirects=True)
    assert response.status_code == 200

    # Return book
    response = client.post("/return", data={"book_id": 1}, follow_redirects=True)
    assert response.status_code == 200
   
