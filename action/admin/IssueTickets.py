# action/admin/IssueTickets.py

from ..Action import Action
from DB_utils import list_events, issue_ticket

class IssueTickets(Action):
    def __init__(self, action_name="Issue Tickets"):
        super().__init__(action_name)

    def exec(self, conn, user=None):
        if user is None or not user.isAdmin():
            conn.send("Unauthorized action.\n".encode('utf-8'))
            return

        # 列出所有活動
        events = list_events()
        if not events:
            conn.send("No events available.\n".encode('utf-8'))
            return
        self.send_table(conn, events)

        # 選擇活動 ID
        event_id_str = self.read_input(conn, "event ID to issue tickets")
        if not event_id_str.isdigit():
            conn.send("Invalid Event ID. Please enter a numeric value.\n".encode('utf-8'))
            return
        event_id = int(event_id_str)

        # 輸入票種
        t_type = self.read_input(conn, "ticket type (e.g., VIP, Regular)")
        if not t_type:
            conn.send("Ticket type cannot be empty.\n".encode('utf-8'))
            return

        # 輸入價格
        price_str = self.read_input(conn, "ticket price")
        try:
            price = float(price_str)
            if price <= 0:
                raise ValueError
        except ValueError:
            conn.send("Invalid price. Please enter a positive number.\n".encode('utf-8'))
            return

        # 輸入總票數
        total_quantity_str = self.read_input(conn, "total quantity")
        if not total_quantity_str.isdigit() or int(total_quantity_str) <= 0:
            conn.send("Invalid quantity. Please enter a positive integer.\n".encode('utf-8'))
            return
        total_quantity = int(total_quantity_str)

        # 發行票券
        success, message = issue_ticket(event_id, t_type, price, total_quantity)
        conn.send(f"{message}\n".encode('utf-8'))
