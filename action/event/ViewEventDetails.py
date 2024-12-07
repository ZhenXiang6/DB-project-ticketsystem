# action/event/ViewEventDetails.py

from DB_utils import view_event_details

def view_event_details_action(e_id):
    event_details = view_event_details(e_id)
    if event_details:
        # 假設 'e_datetime' 是 datetime 對象
        event_details['e_datetime'] = event_details['e_datetime'].isoformat()
    return event_details
