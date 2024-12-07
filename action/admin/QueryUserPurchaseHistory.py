# action/admin/QueryUserPurchaseHistory.py

from ..Action import Action
from DB_utils import query_user_purchase_history

class QueryUserPurchaseHistory(Action):
    def __init__(self, action_name="Query User Purchase History"):
        super().__init__(action_name)

    def exec(self, conn, user=None):
        if user is None or not user.isAdmin():
            conn.send("Unauthorized action.\n".encode('utf-8'))
            return

        # 輸入用戶 ID
        user_id_str = self.read_input(conn, "User ID to query purchase history")
        if not user_id_str.isdigit():
            conn.send("Invalid User ID. Please enter a numeric value.\n".encode('utf-8'))
            return
        user_id = int(user_id_str)

        # 查詢購票紀錄
        history = query_user_purchase_history(user_id)
        if history:
            self.send_table(conn, history)
        else:
            conn.send(f"No purchase history found for User ID: {user_id}\n".encode('utf-8'))
