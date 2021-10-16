from fastapi.testclient import TestClient
from fastapi import status
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post('/users', json={'name': 'testname'})
    assert response.status_code == status.HTTP_201_CREATED

def test_get_user():
    response = client.post('/users', json={'name': 'testname'})
    response = response.json()
    get_user = client.get(f"/users/{response['id']}")
    get_user = get_user.json()
    assert response['name'] == get_user['name']

def test_update_user():
    test_user = client.post('/users', json={'name': 'testname'})
    test_user = test_user.json()
    response = client.put(f"/users/{test_user['id']}", json={"name": "updated_name"})

    get_user = client.get(f"/users/{test_user['id']}")
    get_user = get_user.json()
    assert response.status_code == status.HTTP_200_OK
    assert get_user['name'] == 'updated_name'

def test_delete_user():
    test_user = client.post('/users', json={'name': 'test_delete_user'})
    test_user = test_user.json()

    response = client.delete(f"/users/{test_user['id']}")

    get_user = client.get(f"/users/{test_user['id']}")

    assert response.status_code == status.HTTP_200_OK
    assert get_user.status_code == status.HTTP_404_NOT_FOUND
