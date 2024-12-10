# action/admin/AddEvent.py

from DB_utils import add_event

def add_event_action(e_name, c_name, o_name, e_datetime, e_location, description):
    event_id, message = add_event(e_name, c_name, o_name, e_datetime, e_location, description)
    return event_id, message
