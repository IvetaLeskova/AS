"""Same acceptance criteria for all three architecture variants."""
import pytest


def test_default_priority(client):
    response = client.post('/tasks', json={'title': 'Default priority'})
    assert response.status_code == 201
    assert response.json()['priority'] == 'MEDIUM'


@pytest.mark.parametrize('priority', ['LOW', 'MEDIUM', 'HIGH'])
def test_create_with_priority(client, priority):
    response = client.post('/tasks', json={'title': 'Priority task', 'priority': priority})
    assert response.status_code == 201
    task = response.json()
    assert task['priority'] == priority
    assert client.get('/tasks/' + task['id']).json()['priority'] == priority


def test_update_priority(client):
    created = client.post('/tasks', json={'title': 'Change me'}).json()
    response = client.patch('/tasks/' + created['id'], json={'priority': 'HIGH'})
    assert response.status_code == 200
    assert response.json()['priority'] == 'HIGH'
    assert client.get('/tasks/' + created['id']).json()['priority'] == 'HIGH'


def test_reject_invalid_priority(client):
    response = client.post('/tasks', json={'title': 'Invalid', 'priority': 'URGENT'})
    assert response.status_code == 422
