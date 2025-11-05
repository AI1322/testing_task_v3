import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app, init_db, DB_PATH

@pytest.fixture(scope="module")
def client():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def register_user(client, username="testuser", password="123456"):
    return client.post("/api/register", json={"username": username, "password": password})


def login_user(client, username="testuser", password="123456"):
    return client.post("/api/login", json={"username": username, "password": password})


def test_register_user_success(client):
    r = register_user(client)
    data = r.get_json()
    assert r.status_code == 200
    assert data["success"]


def test_login_success(client):
    r = login_user(client)
    data = r.get_json()
    assert data["success"]
    assert "Sisselogimine" in data["message"]


def test_create_todo_success(client):
    login_user(client)
    r = client.post("/api/todos", json={
        "title": "Write tests",
        "description": "Add pytest cases",
        "priority": "high"
    })
    data = r.get_json()
    assert data["success"]


def test_get_todos_list(client):
    login_user(client)
    r = client.get("/api/todos")
    data = r.get_json()
    assert data["success"]
    assert isinstance(data["todos"], list)
    assert len(data["todos"]) > 0


def test_update_todo_title(client):
    login_user(client)
    todos = client.get("/api/todos").get_json()["todos"]
    todo_id = todos[0]["id"]
    r = client.put(f"/api/todos/{todo_id}", json={"title": "Updated title"})
    data = r.get_json()
    assert data["success"]


def test_delete_todo(client):
    login_user(client)
    todos = client.get("/api/todos").get_json()["todos"]
    todo_id = todos[0]["id"]
    r = client.delete(f"/api/todos/{todo_id}")
    data = r.get_json()
    assert data["success"]


def test_logout(client):
    login_user(client)
    r = client.post("/api/logout")
    data = r.get_json()
    assert data["success"]
