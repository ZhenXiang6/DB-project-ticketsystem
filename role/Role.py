# role/Role.py

class Role:
    def __init__(self, userid, username, pwd, email):
        self.userid = userid
        self.username = username
        self.pwd = pwd
        self.email = email
        self.user_action = []

    def get_available_action(self):
        return self.user_action

    def get_username(self):
        return self.username

    def get_userid(self):
        return self.userid

    def get_email(self):
        return self.email

    def get_info_msg_no_pwd(self):
        return f'User ID: {self.userid}, Username: {self.username}, Email: {self.email}, Role: {type(self).__name__}'

    def get_info_msg(self):
        return f'User ID: {self.userid}, Username: {self.username}, Password: {self.pwd}, Email: {self.email}, Role: {type(self).__name__}'

    def isAdmin(self):
        return False
