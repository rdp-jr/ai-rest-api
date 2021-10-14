from bson.objectid import ObjectId
from app.config import db, logged_in_user_id

test_user = {
        "_id": ObjectId(logged_in_user_id),
        "name": "jdoe",
        "projects": []
    }
    
db.users.insert_one(test_user)