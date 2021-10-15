from fastapi.testclient import TestClient
from fastapi import status
from app.main import app

client = TestClient(app)

def test_create_model():
    project = client.post('/projects', json={'name': 'test_create_model'})
    project_id = project.json()['id']


    test_model = {
        "name": "test_create_model_1",
        "parameters": {
            "batch_size": 32,
            "training_cycles": 32
        }
    }
    
    response = client.post(f'/projects/{project_id}/models', json=test_model)
    
    assert response.status_code == status.HTTP_201_CREATED
    
def test_get_model():
    project = client.post('/projects', json={'name': 'test_get_model_project'})
    project_id = project.json()['id']

    test_model = {
        "name": "test_get_model_1",
        "parameters": {
            "batch_size": 32,
            "training_cycles": 32
        }
    }

    new_model = client.post(f'projects/{project_id}/models', json=test_model)

    new_model_id = new_model.json()['id']
    new_model_name = new_model.json()['name']
    
    
    get_model = client.get(f"/projects/{project_id}/models/{new_model_id}")
    assert get_model.status_code == status.HTTP_200_OK

    get_model = get_model.json()

    assert new_model_name == get_model['name']

def test_update_model():
    
    project = client.post('/projects', json={'name': 'test_update_model_project'})
    project_id = project.json()['id']

    test_model = {
        "name": "test_update_model_1",
        "parameters": {
            "batch_size": 32,
            "training_cycles": 32
        }
    }

    new_model = client.post(f'projects/{project_id}/models', json=test_model)
    new_model_id = new_model.json()['id']
    # new_model_name = new_model.json()['name']

    response = client.put(f"/projects/{project_id}/models/{new_model_id}", json={"name": "test_updated_model_name"})

    get_model = client.get(f"/projects/{project_id}/models/{new_model_id}")
    get_model = get_model.json()

    assert response.status_code == status.HTTP_200_OK
    assert get_model['name'] == 'test_updated_model_name'

    


def test_delete_model():
    project = client.post('/projects', json={'name': 'test_delete_model_project'})
    project_id = project.json()['id']

    test_model = {
        "name": "test_delete_model_1",
        "parameters": {
            "batch_size": 32,
            "training_cycles": 32
        }
    }

    new_model = client.post(f'projects/{project_id}/models', json=test_model)
    new_model_id = new_model.json()['id']

    response = client.delete(f"/projects/{project_id}/models/{new_model_id}")
    assert response.status_code == status.HTTP_200_OK
    
    get_model = client.get(f"/models/{new_model_id}")
    assert get_model.status_code == status.HTTP_404_NOT_FOUND