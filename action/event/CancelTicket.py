# action/event/CancelTicket.py
from ..Action import Action
from DB_utils import list_user_purchases, cancel_ticket

class CancelTicket(Action):
    def exec(self, conn, user):
        # 列出用戶購買的票券
        purchases = list_user_purchases(user.get_userid())
        if not purchases:
            conn.send("You have no tickets to cancel.\n".encode('utf-8'))
            return
        self.send_table(conn, purchases)
        
        # 選擇要取消的訂單 ID
        conn.send("Enter Order ID to cancel: ".encode('utf-8'))
        or_id_str = conn.recv(100).decode('utf-8').strip()
        if not or_id_str.isdigit():
            conn.send("Invalid Order ID. Please enter a numeric value.\n".encode('utf-8'))
            return
        or_id = int(or_id_str)
        
        # 取消訂單
        success, message = cancel_ticket(user.get_userid(), or_id)
        conn.send(f"{message}\n".encode('utf-8'))
