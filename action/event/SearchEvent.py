# action/event/SearchEvent.py

from ..Action import Action
from DB_utils import search_events

class SearchEvent(Action):
    def __init__(self, action_name="Search Events"):
        super().__init__(action_name)

    def exec(self, conn, user=None):
        search_term = self.read_input(conn, "search term (event name or organizer)")
        events = search_events(search_term)
        if events:
            self.send_table(conn, events)
        else:
            conn.send("No events matched your search criteria.\n".encode('utf-8'))
