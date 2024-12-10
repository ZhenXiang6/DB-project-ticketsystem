# action/admin/QueryUserPurchaseHistory.py

from DB_utils import query_user_purchase_history
from utils import serialize_datetimes

def query_user_purchase_history_action(cu_name):
    history = query_user_purchase_history(cu_name)
    if history:
        history = serialize_datetimes(history)
        return history
    return None
