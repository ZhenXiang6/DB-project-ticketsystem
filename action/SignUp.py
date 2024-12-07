# action/SignUp.py

from DB_utils import register_user

def signup_action(username, password, email):
    user_id, message = register_user(username, password, email)
    if user_id:
        return True, {"cu_id": user_id, "message": message}
    else:
        return False, message
