# action/event/ListEvent.py

from DB_utils import list_events

def list_event_action():
    events = list_events()
    return events
