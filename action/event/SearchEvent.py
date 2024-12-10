# action/event/SearchEvent.py

from DB_utils import search_events

def search_event_action(search_term):
    events = search_events(search_term)
    return events
