# action/event/CancelTicket.py

from DB_utils import cancel_ticket

def cancel_ticket_action(or_id, cu_name):
    print(f"Calling cancel_ticket with or_id={or_id} and cu_name={cu_name}")
    success, message = cancel_ticket(or_id, cu_name)
    return success, message
