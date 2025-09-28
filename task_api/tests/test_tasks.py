import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool 
from sqlalchemy.orm import sessionmaker
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.database import Base, get_db
from app.schemas import TaskStatus
from app import models

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool, 
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)



def test_create_task(client):
    """Тест успешного создания задачи."""
    response = client.post(
        "/tasks/",
        json={"title": "Test Task 1", "description": "Description 1"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task 1"
    assert data["description"] == "Description 1"
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data


def test_create_task_missing_title(client):
    """Тест создания задачи без обязательного поля 'title'."""
    response = client.post("/tasks/", json={"description": "Missing title"})
    assert response.status_code == 422


def test_read_tasks_empty(client):
    """Тест получения списка задач, когда база данных пуста."""
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []


def test_read_tasks_with_data(client):
    """Тест получения списка с несколькими задачами."""
    client.post("/tasks/", json={"title": "Task A"})
    client.post("/tasks/", json={"title": "Task B"})

    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task A"
    assert data[1]["title"] == "Task B"


def test_filter_tasks_by_status(client):
    """Тест фильтрации задач по статусу."""
    client.post("/tasks/", json={"title": "Pending Task", "status": "pending"})
    client.post("/tasks/", json={"title": "In Progress Task", "status": "in_progress"})

    response = client.get(f"/tasks/?status={TaskStatus.in_progress.value}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "In Progress Task"

    response = client.get(f"/tasks/?status={TaskStatus.pending.value}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Pending Task"


def test_read_single_task(client):
    """Тест получения одной задачи по её ID."""
    create_response = client.post("/tasks/", json={"title": "My Unique Task"})
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "My Unique Task"
    assert data["id"] == task_id


def test_read_single_task_not_found(client):
    """Тест получения несуществующей задачи."""
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_update_task(client):
    """Тест успешного обновления задачи."""
    create_response = client.post("/tasks/", json={"title": "Old Title"})
    task_id = create_response.json()["id"]

    update_payload = {"title": "New Updated Title", "status": "done"}
    response = client.put(f"/tasks/{task_id}", json=update_payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Updated Title"
    assert data["status"] == "done"
    assert data["id"] == task_id


def test_update_task_not_found(client):
    """Тест обновления несуществующей задачи."""
    response = client.put("/tasks/999", json={"title": "Ghost Task"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_delete_task(client):
    """Тест успешного удаления задачи."""
    create_response = client.post("/tasks/", json={"title": "To Be Deleted"})
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["title"] == "To Be Deleted"

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    """Тест удаления несуществующей задачи."""
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
    