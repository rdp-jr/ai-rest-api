from app.schemas.project import projectsEntity


def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": str(item["name"]),
        "projects": projectsEntity(item["projects"]),
    }

def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]