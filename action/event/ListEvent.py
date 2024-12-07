# action/event/ListEvent.py

from ..Action import Action
from DB_utils import list_available_events

class ListEvent(Action):
    def __init__(self, action_name="List All Available Events"):
        super().__init__(action_name)

    def exec(self, conn, user=None):
        events = list_available_events()
        if events:
            self.send_table(conn, events)
        else:
            conn.send("No available events found.\n".encode('utf-8'))
