# role/User.py

from .Role import Role
from action.Exit import Exit
from action.Logout import Logout
from action.event.ListEvent import ListEvent
from action.ListHistory import ListHistory
from action.event.ViewEventDetails import ViewEventDetails
from action.event.BuyTicket import BuyTicket
from action.event.CancelTicket import CancelTicket
from action.payment.Payment import Payment
from action.user.ViewEditUserInfo import ViewEditUserInfo
from action.user.ViewPurchaseHistory import ViewPurchaseHistory

class User(Role):
    def __init__(self, userid, username, pwd, email):
        super().__init__(userid, username, pwd, email)

        self.user_action = [
            ListEvent("List All Available Events"),
            ViewEventDetails("View Event Details"),
            BuyTicket("Buy Ticket"),
            CancelTicket("Cancel Ticket"),
            Payment("Payment"),
            ViewPurchaseHistory("View Purchase History"),
            ViewEditUserInfo("View/Edit User Information"),
            Logout("Logout"),
            Exit("Leave System")
        ]
