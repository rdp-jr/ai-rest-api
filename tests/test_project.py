from bson.objectid import ObjectId
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.models.project import NewProject, Project
from app.schemas.project import projectEntity

client = TestClient(app)

def test_create_project():
    response = client.post('/projects', json={'name': 'test_create_project'})
    assert response.status_code == status.HTTP_201_CREATED

def test_get_project():
    response = client.post('/projects', json={'name': 'test_get_project'})
    assert response.status_code == status.HTTP_201_CREATED
    
    project_model_id = response.json()['id']
    get_project = client.get(f"/projects/{str(project_model_id)}")
    get_project = get_project.json()

    assert 'test_get_project' == get_project['name']

def test_get_project_nonexistent_id():
    nonexistent_id = '123'
    get_project = client.get(f"/projects/{str(nonexistent_id)}")

    assert get_project.status_code == status.HTTP_404_NOT_FOUND

def test_update_project():
    test_project = client.post('/projects', json={'name': 'test_update_project'})
    test_project = test_project.json()

    response = client.put(f"/projects/{test_project['id']}", json={"name": "test_updated_project_name"})

    get_project = client.get(f"/projects/{test_project['id']}")
    get_project = get_project.json()

    assert response.status_code == status.HTTP_200_OK
    assert get_project['name'] == 'test_updated_project_name'

def test_update_project_nonexistent_id():
    nonexistent_id = '123'
    response = client.put(f"/projects/{nonexistent_id}", json={"name": "test_update_project_nonexistent_id"})
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_project():
    test_project = client.post('/projects', json={'name': 'test_delete_project'})
    test_project = test_project.json()

    response = client.delete(f"/projects/{test_project['id']}")

    get_project = client.get(f"/projects/{test_project['id']}")

    assert response.status_code == status.HTTP_200_OK
    assert get_project.status_code == status.HTTP_404_NOT_FOUND
