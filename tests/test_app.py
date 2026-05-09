from app.app import app

def test_home():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200

def test_get_books():
    client = app.test_client()
    response = client.get("/books")

    assert response.status_code == 200
    assert response.json == [
        {"id": 1, "name": "Atomic Habits"},
        {"id": 2, "name": "Deep Work"}
    ]