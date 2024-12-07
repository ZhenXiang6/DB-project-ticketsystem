# action/LogIn.py

from .Action import Action
from DB_utils import authenticate_user, get_user_role

class LogIn(Action):
    def __init__(self, action_name="Log-in"):
        super().__init__(action_name)

    def exec(self, conn, user=None):
        username = self.read_input(conn, "username")
        password = self.read_input(conn, "password")

        user_id, role = authenticate_user(username, password)
        if user_id is None:
            conn.send("Invalid username or password.\n".encode('utf-8'))
            return None
        else:
            # 根據角色創建 User 或 Admin 實例
            if role == 'Admin':
                from role.Admin import Admin
                return Admin(user_id, username, password, "")
            else:
                from role.User import User
                return User(user_id, username, password, "")
