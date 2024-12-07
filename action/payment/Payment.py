# action/payment/Payment.py

from ..Action import Action
from DB_utils import list_pending_orders, process_payment

class Payment(Action):
    def __init__(self, action_name="Payment"):
        super().__init__(action_name)

    def exec(self, conn, user=None):
        if user is None:
            conn.send("You need to be logged in to make a payment.\n".encode('utf-8'))
            return

        # 列出所有待付款的訂單
        pending_orders = list_pending_orders(user.get_userid())
        if not pending_orders:
            conn.send("You have no pending payments.\n".encode('utf-8'))
            return
        self.send_table(conn, pending_orders)

        # 選擇訂單進行付款
        or_id_str = self.read_input(conn, "Order ID to make payment")
        if not or_id_str.isdigit():
            conn.send("Invalid Order ID. Please enter a numeric value.\n".encode('utf-8'))
            return
        or_id = int(or_id_str)

        # 選擇付款方式
        payment_method = self.read_input(conn, "Payment Method (e.g., Credit Card, PayPal)")
        if not payment_method:
            conn.send("Payment Method cannot be empty.\n".encode('utf-8'))
            return

        # 處理付款
        success, message = process_payment(user.get_userid(), or_id, payment_method)
        conn.send(f"{message}\n".encode('utf-8'))
