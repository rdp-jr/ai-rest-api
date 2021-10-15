from bson.objectid import ObjectId
from fastapi.datastructures import UploadFile
from shortuuid import ShortUUID
from os import unlink
from app.config import logged_in_user_id
from app.models.datasets import Dataset, UpdateDataset
from uuid import uuid4
import shutil

from app.schemas.dataset import DatasetEntity
   
def get_real_dataset_service(db, project_id, real_dataset_id):
    pipeline = [
        {"$match": {'_id': ObjectId(logged_in_user_id), 'projects.real_datasets.id': real_dataset_id}},
        {"$unwind": "$projects"},
        {"$match": {"projects.id": project_id}},
        {"$unwind": "$projects.real_datasets"},
        {"$match": {"projects.real_datasets.id": real_dataset_id}}
    ]
    real_dataset = list(db.users.aggregate(pipeline))

    if real_dataset == []:
        return False

    real_dataset = real_dataset[0]['projects']['real_datasets']

    if not real_dataset:
        return False

    return DatasetEntity(real_dataset)
    

def save_to_file_server_service(file: UploadFile, file_name: str):
    # save file to a cloud storage service like AWS S3
    # bucket = "ai-some-bucket"
    # return f"https://{bucket}.s3-website-ap-southeast-1.amazonaws.com/{file_name}.csv" 

    # for development, save the file to local file system
    with open(f"app/data/{file_name}.csv", 'wb') as out_file:
        shutil.copyfileobj(file.file, out_file)
       
    return f"app/data/{file_name}.csv"

def create_real_dataset_service(db, project_id, file):
    file_name = str(uuid4())
    
    url = save_to_file_server_service(file, file_name)
   
    new_real_dataset = Dataset(id=ShortUUID().random(length=5), name=file_name + "-" + file.filename.split('.')[0], url=url)
    
    result = db.users.update_one(
    {'_id': ObjectId(logged_in_user_id), 'projects.id': project_id },
    {'$push': {'projects.$.real_datasets': new_real_dataset.dict()}}
    )

    if not result.modified_count > 0:
        return False
    
    return new_real_dataset.dict()
    
def check_real_dataset_name_service(db, project_id: str, real_dataset_name: str):
    pass
    if db.users.find_one(
            {'_id': ObjectId(logged_in_user_id), 
            'projects': {
                '$elemMatch': {
                    'id': project_id,
                    'real_datasets': {
                        '$elemMatch': {
                            'name': real_dataset_name
                        }
                    }
                }
            }}
        ):
             
        return False 
    return True

def update_real_dataset_service(db, project_id: str, real_dataset_id: str, req:UpdateDataset):  
    
    result = db.users.update_one(
        {'_id': ObjectId(logged_in_user_id), 'projects.real_datasets.id': real_dataset_id },
        {'$set': {
            'projects.$[i].real_datasets.$[j].name': req.name}
        }, array_filters=[
            {"i.id": project_id}, {"j.id": real_dataset_id}, ]
    )

    if not result.modified_count > 0:
        return False
    
    return get_real_dataset_service(db, project_id, real_dataset_id)

def delete_file_from_file_server(db, project_id, real_dataset_id):
    # delete file from cloud storage
    # for development, delete file from local file system
    dataset = get_real_dataset_service(db, project_id, real_dataset_id)
    unlink(dataset['url'])

def delete_real_dataset_service(db, project_id: str, real_dataset_id: str):

    delete_file_from_file_server(db, project_id, real_dataset_id)
    


    result = db.users.update_one(
    {'_id': ObjectId(logged_in_user_id), 'projects.id': project_id },
    {'$pull': {'projects.$.real_datasets': {"id": real_dataset_id}}}
    )

    if not result.modified_count > 0:
        return False 
    return True