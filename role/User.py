# role/User.py

from .Role import Role
from action.event import (
    buy_ticket_action,
    cancel_ticket_action,
    view_event_details_action,
    list_event_action,
    search_event_action,
    list_categories_action,
    list_event_by_category_action
)
from action.payment import payment_action
from action.user import (
    view_edit_user_info_action,
    view_purchase_history_action
)

class User(Role):
    def __init__(self, cu_id, role):
        super().__init__(cu_id, role)

    def buy_ticket(self, e_id, t_type, quantity):
        return buy_ticket_action(self.cu_id, e_id, t_type, quantity)

    def cancel_ticket(self, or_id):
        return cancel_ticket_action(or_id, self.cu_id)

    def view_event_details(self, e_id):
        return view_event_details_action(e_id)

    def list_events(self):
        return list_event_action()

    def search_event(self, search_term):
        return search_event_action(search_term)

    def list_categories(self):
        return list_categories_action()

    def list_event_by_category(self, c_id):
        return list_event_by_category_action(c_id)

    def make_payment(self, or_id, payment_method, amount):
        return payment_action(or_id, payment_method, amount)

    def view_edit_user_info(self, field, new_value):
        return view_edit_user_info_action(self.cu_id, field, new_value)

    def view_purchase_history(self):
        return view_purchase_history_action(self.cu_id)
