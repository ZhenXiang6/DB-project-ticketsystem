# action/event/ViewEventDetails.py

from DB_utils import view_event_details

def view_event_details_action(e_id):
    event_details = view_event_details(e_id)
    return event_details
