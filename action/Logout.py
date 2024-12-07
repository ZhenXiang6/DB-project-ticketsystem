# action/Logout.py

from .Action import Action

class Logout(Action):
    def __init__(self, action_name="Logout"):
        super().__init__(action_name)

    def exec(self, conn, user=None):
        conn.send("You have been logged out successfully.\n".encode('utf-8'))
        return None  # 返回 None，讓 server.py 處理登出後的流程
