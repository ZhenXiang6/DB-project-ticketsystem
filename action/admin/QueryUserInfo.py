# action/admin/QueryUserInfo.py

from ..Action import Action
from DB_utils import query_user_info

class QueryUserInfo(Action):
    def __init__(self, action_name="Query User Information"):
        super().__init__(action_name)

    def exec(self, conn, user=None):
        if user is None or not user.isAdmin():
            conn.send("Unauthorized action.\n".encode('utf-8'))
            return

        # 輸入用戶 ID
        user_id_str = self.read_input(conn, "User ID to query")
        if not user_id_str.isdigit():
            conn.send("Invalid User ID. Please enter a numeric value.\n".encode('utf-8'))
            return
        user_id = int(user_id_str)

        # 查詢用戶資訊
        user_info = query_user_info(user_id)
        if user_info:
            self.send_table(conn, user_info)
        else:
            conn.send(f"No user found with User ID: {user_id}\n".encode('utf-8'))
