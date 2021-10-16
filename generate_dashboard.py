from starlette.testclient import TestClient
from app.config import db
from app.utils import add_test_user
from io import StringIO

db['users'].drop()
add_test_user()


from app.main import app

client = TestClient(app)


project_1 = client.post('/projects', json={'name': 'project-1'})
project_1 = project_1.json()
project_1['id']

filename = "test_file"
client.post(f"projects/{project_1['id']}/real_datasets",
    files={"file": (filename, StringIO("csv data here"), "rb")})
client.post(f"projects/{project_1['id']}/real_datasets",
    files={"file": (filename, StringIO("csv data here"), "rb")})
client.post(f"projects/{project_1['id']}/real_datasets",
    files={"file": (filename, StringIO("csv data here"), "rb")})



test_model = {
        "name": "model_1",
        "parameters": {
            "batch_size": 32,
            "training_cycles": 32
        }
    }

new_model = client.post(f"projects/{project_1['id']}/models", json=test_model)
new_model = new_model.json()
client.post(f"/projects/{project_1['id']}/models/{new_model['id']}/synthetic_datasets")
client.post(f"/projects/{project_1['id']}/models/{new_model['id']}/synthetic_datasets")

test_model = {
        "name": "model_2",
        "parameters": {
            "batch_size": 64,
            "training_cycles": 64
        }
    }

new_model = client.post(f"projects/{project_1['id']}/models", json=test_model)
new_model = new_model.json()
client.post(f"/projects/{project_1['id']}/models/{new_model['id']}/synthetic_datasets")
client.post(f"/projects/{project_1['id']}/models/{new_model['id']}/synthetic_datasets")




project_2 = client.post('/projects', json={'name': 'project-2'})
project_2 = project_2.json()
client.post(f"projects/{project_2['id']}/real_datasets",
    files={"file": (filename, StringIO("csv data here"), "rb")})
client.post(f"projects/{project_2['id']}/real_datasets",
    files={"file": (filename, StringIO("csv data here"), "rb")})


test_model = {
        "name": "model_1_lorem",
        "parameters": {
            "batch_size": 32,
            "training_cycles": 32
        }
    }

new_model = client.post(f"projects/{project_2['id']}/models", json=test_model)

new_model = new_model.json()
client.post(f"/projects/{project_2['id']}/models/{new_model['id']}/synthetic_datasets")
client.post(f"/projects/{project_2['id']}/models/{new_model['id']}/synthetic_datasets")

test_model = {
        "name": "model_2_ipsum",
        "parameters": {
            "batch_size": 128,
            "training_cycles": 128
        }
    }

new_model = client.post(f"projects/{project_2['id']}/models", json=test_model)

new_model = new_model.json()
client.post(f"/projects/{project_2['id']}/models/{new_model['id']}/synthetic_datasets")
client.post(f"/projects/{project_2['id']}/models/{new_model['id']}/synthetic_datasets")
client.post(f"/projects/{project_2['id']}/models/{new_model['id']}/synthetic_datasets")


test_model = {
        "name": "model_3_empty_synthetic_data_example",
        "parameters": {
            "batch_size": 64,
            "training_cycles": 64
        }
    }

new_model = client.post(f"projects/{project_2['id']}/models", json=test_model)


project_3 = client.post('/projects', json={'name': 'project-3-empty-project-example'})