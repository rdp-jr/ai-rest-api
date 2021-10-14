def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": str(item["name"])
    }

def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]