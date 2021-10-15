from bson.objectid import ObjectId
from app.schemas.user import userEntity, usersEntity
from app.models.user import NewUser, UpdateUser, User

def get_users_service(db):
    users = usersEntity(db.users.find())
    return users

def get_user_service(db, user_id):
    user = userEntity(db.users.find_one({"_id": ObjectId(user_id)}))
    if not user:
        return False 
    return user

def create_user_service(db, req: NewUser):
    data = req.dict(exclude_unset=True)
    new_user = User(**data)
    
    result = db.users.insert_one(new_user.dict())
    user = userEntity(db.users.find_one({"_id": result.inserted_id}))
    return user

def update_user_service(db, user_id, req:UpdateUser):
    if not db.users.find_one(
        {'_id': ObjectId(user_id)}):
             
        return 404
    
    db.users.update_one(
    {'_id': ObjectId(user_id)},
    {'$set': {'name': req.name}}
    )