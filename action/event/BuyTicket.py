# action/event/BuyTicket.py

from DB_utils import buy_ticket

def buy_ticket_action(cu_id, e_id, t_type, quantity):
    success, message = buy_ticket(cu_id, e_id, t_type, quantity)
    return success, message
