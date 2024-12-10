# utils.py

from datetime import datetime
from decimal import Decimal

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
    elif isinstance(obj, tuple):
        return tuple(serialize_datetimes(item) for item in obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return str(obj)  # 使用 str 保持精度
    else:
        return obj
