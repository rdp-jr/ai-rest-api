def ModelEntity(item) -> dict:
    return {
        "id": str(item["id"]),
        "name": str(item["name"]),
        "parameters": ModelParameterEntity(item["parameters"])
    }

def ModelParameterEntity(item) -> dict:
    return {
        "batch_size": int(item["batch_size"]),
        "training_cycles": int(item["training_cycles"])
    }