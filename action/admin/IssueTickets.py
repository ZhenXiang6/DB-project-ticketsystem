# action/admin/IssueTickets.py

from DB_utils import issue_ticket

def issue_tickets_action(e_id, t_type, price, total_quantity):
    success, message = issue_ticket(e_id, t_type, price, total_quantity)
    return success, message
