# action/event/ListEventByCategory.py

from DB_utils import list_event_by_category

def list_event_by_category_action(c_id):
    return list_event_by_category(c_id)
