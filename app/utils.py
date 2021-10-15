from bson.objectid import ObjectId
from app.config import db, logged_in_user_id

def get_db():
    yield db

def add_test_user():
    test_user = {
            "_id": ObjectId(logged_in_user_id),
            "name": "jdoe",
            "projects": []
        }
        
    db.users.insert_one(test_user)