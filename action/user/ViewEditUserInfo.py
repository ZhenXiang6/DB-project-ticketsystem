# action/user/ViewEditUserInfo.py

from DB_utils import view_edit_user_info

def view_edit_user_info_action(cu_id, field, new_value):
    success, message = view_edit_user_info(cu_id, field, new_value)
    return success, message
