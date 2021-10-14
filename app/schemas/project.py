def projectEntity(item) -> dict:
    return {
        "id": str(item["id"]),
        "name": str(item["name"]),
        "models": list(item["models"]),
        "real_datasets": list(item["real_datasets"]),
        
    }

def projectsEntity(entity) -> list:
    return [projectEntity(item) for item in entity]