# action/Exit.py

from .Action import Action

class Exit(Action):
    def __init__(self, action_name="Exit"):
        super().__init__(action_name)

    def exec(self, conn, user=None):
        conn.send("[EXIT]Exiting the system. Goodbye!\n".encode('utf-8'))
        return -1  # 特殊返回值，用於終止連接
