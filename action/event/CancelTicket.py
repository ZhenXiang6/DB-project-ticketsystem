# action/event/CancelTicket.py

from DB_utils import cancel_ticket

def cancel_ticket_action(or_id, cu_id):
    success, message = cancel_ticket(or_id, cu_id)
    return success, message
