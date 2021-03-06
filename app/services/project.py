from bson.objectid import ObjectId
from shortuuid.main import ShortUUID
from app.schemas.project import projectEntity, projectsEntity
from app.models.project import NewProject, UpdateProject, Project
from app.config import logged_in_user_id
from app.services.model import delete_model_service, get_models_service
from app.services.real_dataset import delete_real_dataset_service, get_real_datasets_service

def get_projects_service(db):
    user = db.users.find_one({"_id": ObjectId(logged_in_user_id)})

    if not user:
        return False
    return projectsEntity(user['projects'])
   
def get_project_service(db, project_id):
    project = db.users.find_one(
        {"_id": ObjectId(logged_in_user_id), "projects.id": project_id}, 
        {"projects.$": True}
    )

    if not project:
        return False

    return projectEntity(project['projects'][0])
        

def create_project_service(db, req: NewProject):
    data = req.dict(exclude_unset=True)
        
    new_project = Project(**data, id=ShortUUID().random(length=5))

    result = db.users.update_one(
    {"_id": ObjectId(logged_in_user_id) },
    {"$push": {"projects": new_project.dict()}}
    )
    
    if result.modified_count > 0:
        project = projectEntity(new_project.dict())
        return project
        
    return False

def check_project_name_service(db, project_name):
    if db.users.find_one(
            {'_id': ObjectId(logged_in_user_id), 
            'projects': {
                '$elemMatch': {
                    'name': project_name
                }
            }}
        ):
             
        return False 
    return True

def update_project_service(db, project_id, req:UpdateProject):    
    db.users.update_one(
        {'_id': ObjectId(logged_in_user_id), 'projects.id': project_id },
        {'$set': {'projects.$.name': req.name}}
    )

def delete_project_service(db, project_id):

    models = get_models_service(db, project_id)

    if isinstance(models, list):
        for model in models:
            delete_model_service(db, project_id, model['id'])

    real_datasets = get_real_datasets_service(db, project_id)

    if isinstance(real_datasets, list):
        for real_dataset in real_datasets:
            delete_real_dataset_service(db, project_id, real_dataset['id'])


    result = db.users.update_one(
    {'_id': ObjectId(logged_in_user_id) },
    {'$pull': {'projects': {"id": project_id}}}
    )

    if not result.modified_count > 0:
        return False 
    return True