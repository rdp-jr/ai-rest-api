def modelEntity(item) -> dict:
    return {
        "id": str(item["id"]),
        "name": str(item["name"]),
        "parameters": modelParameterEntity(item["parameters"])
    }

def modelsEntity(entity) -> list:
    return [modelEntity(item) for item in entity]


def modelParameterEntity(item) -> dict:
    return {
        "batch_size": int(item["batch_size"]),
        "training_cycles": int(item["training_cycles"])
    }