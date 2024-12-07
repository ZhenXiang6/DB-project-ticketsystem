# action/ListHistory.py

from .Action import Action
from DB_utils import list_user_purchases_history

class ListHistory(Action):
    def __init__(self, action_name="List History"):
        super().__init__(action_name)

    def exec(self, conn, user=None):
        if user is None:
            conn.send("You need to be logged in to view history.\n".encode('utf-8'))
            return

        history = list_user_purchases_history(user.get_userid())
        if history:
            self.send_table(conn, history)
        else:
            conn.send("No purchase history found.\n".encode('utf-8'))
