# action/event/ListEvent.py

from DB_utils import list_events
from utils import serialize_datetimes

def list_event_action():
    events = list_events()
    if events:
        events = serialize_datetimes(events)
    return events
