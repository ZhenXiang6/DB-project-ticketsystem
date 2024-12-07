# role/Admin.py

from .User import User
from action.admin.IssueTickets import IssueTickets
from action.admin.AddEvent import AddEvent
from action.admin.QueryUserInfo import QueryUserInfo
from action.admin.QueryUserPurchaseHistory import QueryUserPurchaseHistory

class Admin(User):
    def __init__(self, userid, username, pwd, email):
        super().__init__(userid, username, pwd, email)
        self.user_action += [
            IssueTickets("Issue Tickets"),
            AddEvent("Add Event"),
            QueryUserInfo("Query User Information"),
            QueryUserPurchaseHistory("Query User Purchase History")
        ]

    def isAdmin(self):
        return True
