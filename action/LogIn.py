# action/LogIn.py

from DB_utils import authenticate_user

def login_action(username, password):
    user_id, role = authenticate_user(username, password)
    if user_id:
        return True, {"cu_id": user_id, "role": role}
    else:
        return False, "Invalid username or password."
