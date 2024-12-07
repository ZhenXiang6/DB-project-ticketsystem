# utils.py

def format_response(data):
    if isinstance(data, list):
        return "\n".join([str(item) for item in data])
    elif isinstance(data, dict):
        return "\n".join([f"{key}: {value}" for key, value in data.items()])
    else:
        return str(data)
