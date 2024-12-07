# action/SignUp.py

from .Action import Action
from DB_utils import register_user, username_exists

class SignUp(Action):
    def __init__(self, action_name="Sign-up"):
        super().__init__(action_name)

    def exec(self, conn, user=None):
        username = self.read_input(conn, "new username")
        password = self.read_input(conn, "new password")
        email = self.read_input(conn, "email")

        if username_exists(username):
            conn.send("Username already exists. Please try a different one.\n".encode('utf-8'))
            return None

        user_id = register_user(username, password, email)
        if user_id:
            conn.send(f"User registered successfully with User ID: {user_id}\n".encode('utf-8'))
            return None
        else:
            conn.send("Registration failed. Please try again.\n".encode('utf-8'))
            return None
