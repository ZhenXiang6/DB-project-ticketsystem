# role/Admin.py

from .Role import Role
from action.admin import (
    add_event_action,
    issue_tickets_action,
    query_user_info_action,
    query_user_purchase_history_action,
    generate_sales_report_action
)

class Admin(Role):
    def __init__(self, cu_id, role):
        super().__init__(cu_id, role)

    def add_event(self, e_name, c_id, o_name, e_datetime, e_location, description):
        return add_event_action(e_name, c_id, o_name, e_datetime, e_location, description)

    def issue_tickets(self, e_id, t_type, price, total_quantity):
        return issue_tickets_action(e_id, t_type, price, total_quantity)

    def query_user_info(self, cu_id):
        return query_user_info_action(cu_id)

    def query_user_purchase_history(self, cu_id):
        return query_user_purchase_history_action(cu_id)

    def get_sales_report(self, e_id):
        return generate_sales_report_action(e_id)