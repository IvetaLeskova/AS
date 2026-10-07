from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


TEST_DATABASE_URL = "sqlite://"


engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Finish architecture project",
            "description": "Implement layered Task Manager"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Finish architecture project"
    assert data["description"] == "Implement layered Task Manager"
    assert data["status"] == "TODO"

    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_create_task_with_empty_title():
    response = client.post(
        "/tasks",
        json={
            "title": "",
            "description": "Invalid task"
        }
    )

    assert response.status_code == 422

def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

def test_get_task():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Test task",
            "description": "Task for GET test"
        }
    )

    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Test task"

def test_get_non_existing_task():
    response = client.get(
        "/tasks/non-existing-id"
    )

    assert response.status_code == 404

def test_change_task_status():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Status test"
        }
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}/status",
        json={
            "status": "DONE"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "DONE"

def test_update_task():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Old title"
        }
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "title": "New title"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New title"

def test_delete_task():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Task to delete"
        }
    )

    task_id = create_response.json()["id"]

    response = client.delete(
        f"/tasks/{task_id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/tasks/{task_id}"
    )

    assert get_response.status_code == 404

def test_task_summary():
    response = client.get("/tasks/summary")

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "todo" in data
    assert "done" in data

    assert data["total"] == data["todo"] + data["done"]

