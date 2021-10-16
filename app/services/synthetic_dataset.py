from bson.objectid import ObjectId
from shortuuid import ShortUUID
from os import unlink
from app.config import logged_in_user_id
from app.models.datasets import Dataset
from uuid import uuid4
import shutil
from app.models.model import UpdateModel
from app.schemas.dataset import datasetEntity, datasetsEntity

def get_synthetic_datasets_service(db, project_id, model_id):
    pipeline = [
        {"$match": {'_id': ObjectId(logged_in_user_id), 'projects.models.id': model_id }},
        {"$unwind": "$projects"},
        {"$match": {"projects.id": project_id}},
        {"$unwind": "$projects.models"},
        {"$match": {"projects.models.id": model_id}}
    ]
    synthetic_datasets = list(db.users.aggregate(pipeline))
    
    if synthetic_datasets == []:
        return False

    synthetic_datasets = synthetic_datasets[0]['projects']['models']['synthetic_datasets']

    return datasetsEntity(synthetic_datasets)


def get_synthetic_dataset_service(db, project_id, model_id, synthetic_dataset_id):
    
    pipeline = [
        {"$match": {'_id': ObjectId(logged_in_user_id), 'projects.models.id': model_id, 'projects.models.synthetic_datasets.id': synthetic_dataset_id}},
        {"$unwind": "$projects"},
        {"$match": {"projects.id": project_id}},
        {"$unwind": "$projects.models"},
        {"$match": {"projects.models.id": model_id}},
        {"$unwind": "$projects.models.synthetic_datasets"},
        {"$match": {"projects.models.synthetic_datasets.id": synthetic_dataset_id}},
    ]
    synthetic_dataset = list(db.users.aggregate(pipeline))
    
    if synthetic_dataset == []:
        return False

    synthetic_dataset = synthetic_dataset[0]['projects']['models']['synthetic_datasets']

    return datasetEntity(synthetic_dataset)
    

def generate_synthetic_data():
    # Interface with the AI service
    # send real datasets (csv files)
    # receive a synthetic dataset (csv file) back
    # save csv file to cloud storage

    # for development, we simply make a copy of a template synthetic dataset (50 rows)
    # and save it in the local file system
    file_name = str(uuid4())
    synthetic_file = {
        "name": file_name,
        "url": f"app/data/{file_name}.csv"
    }
    shutil.copyfile("app/data/synthetic_dataset_template.csv", f"app/data/{file_name}.csv")
       
    return synthetic_file


def create_synthetic_dataset_service(db, project_id: str, model_id: str):
    synthetic_file = generate_synthetic_data()
    new_synthetic_dataset = Dataset(id=ShortUUID().random(length=5), name=synthetic_file["name"], url=synthetic_file["url"])

    result = db.users.update_one(
        {'_id': ObjectId(logged_in_user_id), 'projects.id': project_id, 'projects.models.id': model_id },
        {'$push': {
        'projects.$[i].models.$[j].synthetic_datasets': 
        new_synthetic_dataset.dict()
        }
    }, array_filters=[{
        "i.id": project_id
    }, {"j.id": model_id}]
    )

    if not result.modified_count > 0:
        return False
    
    return new_synthetic_dataset.dict()
    
    
def check_synthetic_dataset_name_service(db, project_id, model_id, synthetic_dataset_name):
    if db.users.find_one(
            {'_id': ObjectId(logged_in_user_id), 
            'projects': {
                '$elemMatch': {
                    'id': project_id,
                    'models': {
                        'id': model_id,
                        '$elemMatch': {
                            'synthetic_datasets': {
                                'id': synthetic_dataset_name
                            }
                        }
                    }
                }
            }}
        ):
             
        return False 
    return True

def update_synthetic_dataset_service(db, project_id: str, model_id: str, synthetic_dataset_id: str, req:UpdateModel):  
    
    result = db.users.update_one(
        {'_id': ObjectId(logged_in_user_id), 'projects.models.id': model_id },
        {'$set': {
            'projects.$[i].models.$[j].synthetic_datasets.$[k].name': req.name}
        }, array_filters=[
            {"i.id": project_id}, {"j.id": model_id}, {"k.id": synthetic_dataset_id},]
    )

    if not result.modified_count > 0:
        return False
    
    return get_synthetic_dataset_service(db, project_id, model_id, synthetic_dataset_id)
    
def delete_file_from_file_server(db, project_id, model_id, synthetic_dataset_id):
    dataset = get_synthetic_dataset_service(db, project_id, model_id, synthetic_dataset_id)
    unlink(dataset['url'])


def delete_synthetic_dataset_service(db, project_id: str, model_id: str, synthetic_dataset_id: str):
    
    delete_file_from_file_server(db, project_id, model_id, synthetic_dataset_id)
    
    result = db.users.update_one(
    {'_id': ObjectId(logged_in_user_id), 'projects.id': project_id, 'projects.models.id': model_id },
    {'$pull': {'projects.$[i].models.$[j].synthetic_datasets': {"id": synthetic_dataset_id}}}, 
    array_filters=[
        {"i.id": project_id}, {"j.id": model_id}]
    )

    if not result.modified_count > 0:
        return False 
    return True