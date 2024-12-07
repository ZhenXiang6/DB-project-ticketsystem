# action/admin/QueryUserInfo.py

from DB_utils import query_user_info

def query_user_info_action(cu_id):
    user_info = query_user_info(cu_id)
    return user_info
