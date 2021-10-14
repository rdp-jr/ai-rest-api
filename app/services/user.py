from app.schemas.user import usersEntity
from app.models.user import User

def get_users(db):
    users = usersEntity(db.users.find())
    return users


def insert_user(db, req: User):
    print('inserting user from service')
    db.users.insert_one(req.dict())
    return True