# action/admin/QueryUserPurchaseHistory.py

from DB_utils import query_user_purchase_history

def query_user_purchase_history_action(cu_id):
    history = query_user_purchase_history(cu_id)
    return history
