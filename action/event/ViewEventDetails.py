# action/event/ViewEventDetails.py
from ..Action import Action
from DB_utils import get_event_details

class ViewEventDetails(Action):
    def exec(self, conn, user):
        conn.send("Enter Event ID to view details: ".encode('utf-8'))
        event_id_str = conn.recv(100).decode('utf-8').strip()
        if not event_id_str.isdigit():
            conn.send("Invalid Event ID. Please enter a numeric value.\n".encode('utf-8'))
            return
        event_id = int(event_id_str)
        
        event_details = get_event_details(event_id)
        if not event_details:
            conn.send(f"No event found with ID: {event_id}\n".encode('utf-8'))
            return
        self.send_table(conn, event_details)
