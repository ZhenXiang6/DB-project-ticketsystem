# action/event/BuyTicket.py
from ..Action import Action
from DB_utils import list_available_events, list_ticket_types, purchase_ticket

class BuyTicket(Action):
    def exec(self, conn, user):
        # 列出所有可用活動
        events = list_available_events()
        if not events:
            conn.send("No available events to purchase tickets.\n".encode('utf-8'))
            return
        self.send_table(conn, events)
        
        # 選擇活動
        conn.send("Enter Event ID to purchase ticket: ".encode('utf-8'))
        event_id_str = conn.recv(100).decode('utf-8').strip()
        if not event_id_str.isdigit():
            conn.send("Invalid Event ID. Please enter a numeric value.\n".encode('utf-8'))
            return
        event_id = int(event_id_str)
        
        # 列出票種
        ticket_types = list_ticket_types(event_id)
        if not ticket_types:
            conn.send("No ticket types available for this event.\n".encode('utf-8'))
            return
        self.send_table(conn, ticket_types)
        
        # 選擇票種
        conn.send("Enter Ticket Type: ".encode('utf-8'))
        t_type = conn.recv(100).decode('utf-8').strip()
        
        # 選擇數量
        conn.send("Enter Quantity: ".encode('utf-8'))
        quantity_str = conn.recv(100).decode('utf-8').strip()
        if not quantity_str.isdigit() or int(quantity_str) <= 0:
            conn.send("Invalid quantity. Please enter a positive integer.\n".encode('utf-8'))
            return
        quantity = int(quantity_str)
        
        # 購買票券
        success, message = purchase_ticket(user.get_userid(), event_id, t_type, quantity)
        conn.send(f"{message}\n".encode('utf-8'))
