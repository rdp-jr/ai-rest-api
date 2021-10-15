from io import StringIO
from os import unlink
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app

client = TestClient(app)

def test_create_real_dataset():
    project = client.post('/projects', json={'name': 'test_create_real_dataset'})
    project_id = project.json()['id']

    filename = "test_file"
    response = client.post(f'projects/{project_id}/real_datasets', 
        files={"file": (filename, StringIO("csv data here"), "rb")})
    
    assert response.status_code == status.HTTP_201_CREATED
    response = response.json()
    unlink(response['url'])

def test_get_real_dataset():
    project = client.post('/projects', json={'name': 'test_get_real_dataset_project'})
    project_id = project.json()['id']

    filename = "test_file"
    test_real_dataset = client.post(f'/projects/{project_id}/real_datasets', 
        files={"file": (filename, StringIO("csv data here"), "rb")})

    test_real_dataset_id = test_real_dataset.json()['id']
    test_real_dataset_name = test_real_dataset.json()['name']
    
    
    get_real_dataset = client.get(f"/real_datasets/{test_real_dataset_id}")
    assert get_real_dataset.status_code == status.HTTP_200_OK

    get_real_dataset = get_real_dataset.json()

    assert test_real_dataset_name == get_real_dataset['name']

    unlink(get_real_dataset['url'])

# def test_get_project_nonexistent_id():
#     nonexistent_id = '123'
#     get_project = client.get(f"/projects/{str(nonexistent_id)}")

#     assert get_project.status_code == status.HTTP_404_NOT_FOUND

def test_update_real_dataset():
    
    project = client.post('/projects', json={'name': 'test_update_real_dataset_project'})
    project_id = project.json()['id']

    filename = "test_file"
    test_real_dataset = client.post(f'projects/{project_id}/real_datasets', 
        files={"file": (filename, StringIO("csv data here"), "rb")})
    test_real_dataset = test_real_dataset.json()

    response = client.put(f"/projects/{project_id}/real_datasets/{test_real_dataset['id']}", json={"name": "test_updated_real_dataset_name"})

    get_real_dataset = client.get(f"/real_datasets/{test_real_dataset['id']}")
    get_real_dataset = get_real_dataset.json()

    assert response.status_code == status.HTTP_200_OK
    assert get_real_dataset['name'] == 'test_updated_real_dataset_name'

    unlink(get_real_dataset['url'])


def test_delete_real_dataset():
    project = client.post('/projects', json={'name': 'test_delete_real_dataset_project'})
    project_id = project.json()['id']

    filename = "test_file"
    test_real_dataset = client.post(f'/projects/{project_id}/real_datasets', 
        files={"file": (filename, StringIO("csv data here"), "rb")})
    test_real_dataset = test_real_dataset.json()

    response = client.delete(f"/projects/{project_id}/real_datasets/{test_real_dataset['id']}")
    assert response.status_code == status.HTTP_200_OK
    
    get_real_dataset = client.get(f"/real_datasets/{test_real_dataset['id']}")
   
    assert get_real_dataset.status_code == status.HTTP_404_NOT_FOUND