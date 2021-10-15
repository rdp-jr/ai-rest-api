from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from os import unlink

client = TestClient(app)

def test_create_synthetic_dataset():
    project = client.post('/projects', json={'name': 'test_create_synthetic_dataset'})
    project_id = project.json()['id']

    model_data = {
        "name": "test_create_synthetic_dataset_1",
        "parameters": {
            "batch_size": 32,
            "training_cycles": 32
        }
    }
    
    model = client.post(f'/projects/{project_id}/models', json=model_data)
    model_id = model.json()['id']

    response = client.post(f'/projects/{project_id}/models/{model_id}/synthetic_datasets')
    assert response.status_code == status.HTTP_201_CREATED

    response = response.json()
    unlink(response['url'])
    
def test_get_synthetic_dataset():
    project = client.post('/projects', json={'name': 'test_get_synthetic_dataset'})
    project_id = project.json()['id']

    model_data = {
        "name": "test_get_synthetic_dataset_1",
        "parameters": {
            "batch_size": 32,
            "training_cycles": 32
        }
    }
    
    model = client.post(f'/projects/{project_id}/models', json=model_data)
    model_id = model.json()['id']

    new_synthetic_dataset = client.post(f'/projects/{project_id}/models/{model_id}/synthetic_datasets')

    new_synthetic_dataset_id = new_synthetic_dataset.json()['id']
    new_synthetic_dataset_name = new_synthetic_dataset.json()['name']
    
    
    get_synthetic_dataset = client.get(f"/projects/{project_id}/models/{model_id}/synthetic_datasets/{new_synthetic_dataset_id}")
    assert get_synthetic_dataset.status_code == status.HTTP_200_OK

    get_synthetic_dataset = get_synthetic_dataset.json()

    assert new_synthetic_dataset_name == get_synthetic_dataset['name']

    unlink(get_synthetic_dataset['url'])
    

def test_update_synthetic_dataset():
    
    project = client.post('/projects', json={'name': 'test_update_synthetic_dataset_project'})
    project_id = project.json()['id']

    model_data = {
        "name": "test_update_synthetic_dataset_1",
        "parameters": {
            "batch_size": 32,
            "training_cycles": 32
        }
    }
    model = client.post(f'/projects/{project_id}/models', json=model_data)
    model_id = model.json()['id']

    new_synthetic_dataset = client.post(f'/projects/{project_id}/models/{model_id}/synthetic_datasets')
    new_synthetic_dataset_id = new_synthetic_dataset.json()['id']
   
    response = client.put(f"/projects/{project_id}/models/{model_id}/synthetic_datasets/{new_synthetic_dataset_id}", json={"name": "test_updated_synthetic_dataset_name"})

    assert response.status_code == status.HTTP_200_OK

    response = response.json()
    assert response['name'] == 'test_updated_synthetic_dataset_name'

    unlink(response['url'])

    


def test_delete_synthetic_dataset():
    project = client.post('/projects', json={'name': 'test_delete_synthetic_dataset_project'})
    project_id = project.json()['id']

    model_data = {
        "name": "test_delete_synthetic_dataset_1",
        "parameters": {
            "batch_size": 32,
            "training_cycles": 32
        }
    }
    model = client.post(f'/projects/{project_id}/models', json=model_data)
    model_id = model.json()['id']

    new_synthetic_dataset = client.post(f'/projects/{project_id}/models/{model_id}/synthetic_datasets')
    new_synthetic_dataset_id = new_synthetic_dataset.json()['id']
   
    response = client.delete(f"/projects/{project_id}/models/{model_id}/synthetic_datasets/{new_synthetic_dataset_id}", json={"name": "test_updated_synthetic_dataset_name"})

    assert response.status_code == status.HTTP_200_OK

    response = response.json()
    

    get_synthetic_dataset = client.get(f"/projects/{project_id}/models/{model_id}/synthetic_datasets/{new_synthetic_dataset_id}")
    assert get_synthetic_dataset.status_code == status.HTTP_404_NOT_FOUND