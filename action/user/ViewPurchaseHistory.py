# action/user/ViewPurchaseHistory.py
from ..Action import Action
from DB_utils import list_user_purchases_history

class ViewPurchaseHistory(Action):
    def exec(self, conn, user):
        history = list_user_purchases_history(user.get_userid())
        if not history:
            conn.send("You have no purchase history.\n".encode('utf-8'))
            return
        self.send_table(conn, history)
