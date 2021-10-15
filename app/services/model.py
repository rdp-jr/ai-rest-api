from bson.objectid import ObjectId
from fastapi.datastructures import UploadFile
from shortuuid import ShortUUID
from os import unlink
from app.config import logged_in_user_id
from app.models.model import Model, ModelParameter, NewModel, UpdateModel
from uuid import uuid4

from app.schemas.model import ModelEntity

def get_model_service(db, project_id, model_id):
    
    pipeline = [
        {"$match": {'_id': ObjectId(logged_in_user_id), 'projects.models.id': model_id}},
        {"$unwind": "$projects"},
        {"$match": {"projects.id": project_id}},
        {"$unwind": "$projects.models"},
        {"$match": {"projects.models.id": model_id}}
    ]
    model = list(db.users.aggregate(pipeline))

    if model == []:
        return False

    model = model[0]['projects']['models']

    return ModelEntity(model)
    



def create_model_service(db, project_id: str, req: NewModel):
    data = req.dict(exclude_unset=True)
    new_model = Model(id=ShortUUID().random(length=5), 
                    name=data['name'], 
                    parameters=ModelParameter(batch_size=data['parameters']['batch_size'], 
                                            training_cycles=data['parameters']['training_cycles']))

    result = db.users.update_one(
        {'_id': ObjectId(logged_in_user_id), 'projects.id': project_id },
        {'$push': {'projects.$.models': new_model.dict()}}
    )

    if not result.modified_count > 0:
        return False
    
    return new_model.dict()
    
    
def check_model_name_service(db, project_id, model_name):
    if db.users.find_one(
            {'_id': ObjectId(logged_in_user_id), 
            'projects': {
                '$elemMatch': {
                    'id': project_id,
                    'models': {
                        '$elemMatch': {
                            'name': model_name
                        }
                    }
                }
            }}
        ):
             
        return False 
    return True

def update_model_service(db, project_id: str, model_id: str, req:UpdateModel):  
    
    result = db.users.update_one(
        {'_id': ObjectId(logged_in_user_id), 'projects.models.id': model_id },
        {'$set': {
            'projects.$[i].models.$[j].name': req.name}
        }, array_filters=[
            {"i.id": project_id}, {"j.id": model_id}, ]
    )

    if not result.modified_count > 0:
        return False
    
    return get_model_service(db, project_id, model_id)
    



def delete_model_service(db, project_id: str, model_id: str):
    result = db.users.update_one(
    {'_id': ObjectId(logged_in_user_id), 'projects.id': project_id },
    {'$pull': {'projects.$.models': {"id": model_id}}}
    )

    if not result.modified_count > 0:
        return False 
    return True