# action/ListHistory.py

from DB_utils import list_history

def list_history_action(cu_id):
    history = list_history(cu_id)
    return history
