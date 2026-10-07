from fastapi.testclient import TestClient

from app.main import app


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