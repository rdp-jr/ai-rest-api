from fastapi.testclient import TestClient
from fastapi import status

from app.main import app

def test_create_user():
    client = TestClient(app)
    response = client.post('/users', json={'name': 'testname'})
    assert response.status_code == status.HTTP_201_CREATED