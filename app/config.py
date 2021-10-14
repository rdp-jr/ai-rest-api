testing = True 
logged_in_user_id = "61642328d0b56917037c40ad"
mongodb_url = "mongodb://localhost:27017"


from pymongo import MongoClient

client = MongoClient(mongodb_url) 


if testing:
    db = client.ai_users_test
else:
    db = client.ai_users 

