# utils.py

from datetime import datetime
def format_response(data):
    if isinstance(data, list):
        return "\n".join([str(item) for item in data])
    elif isinstance(data, dict):
        return "\n".join([f"{key}: {value}" for key, value in data.items()])
    else:
        return str(data)
def serialize_datetimes(obj):
    if isinstance(obj, dict):
        return {k: serialize_datetimes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_datetimes(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj