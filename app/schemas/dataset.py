def DatasetEntity(item) -> dict:
    return {
        "id": str(item["id"]),
        "name": str(item["name"]),
        "url": str(item["url"]),
    }