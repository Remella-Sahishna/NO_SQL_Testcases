import pytest # type: ignore
from chatbot import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

def test_books_page(client):
    response = client.get("/books")
    # Redirect to login if not logged in
    assert response.status_code in [200, 302]

def test_add_book_page_requires_login(client):
    response = client.get("/add_book")
    assert response.status_code == 302  # redirect to login

def test_add_book_post(client):
    # Simulate login first
    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.post("/add_book", data={
        "title": "Test Book",
        "authors": "Author1, Author2",
        "genres": "Fiction, Adventure",
        "copies": "5"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"has been added successfully" in response.data

def test_book_detail_requires_login(client):
    response = client.get("/books/1")
    assert response.status_code == 302  # redirects to login
