from bson import ObjectId


def object_id_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, dict):
        return {k: object_id_to_str(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [object_id_to_str(i) for i in obj]
    return obj
