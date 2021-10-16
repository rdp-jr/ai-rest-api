def datasetEntity(item) -> dict:
    return {
        "id": str(item["id"]),
        "name": str(item["name"]),
        "url": str(item["url"]),
    }

def datasetsEntity(entity) -> list:
    return [datasetEntity(item) for item in entity]