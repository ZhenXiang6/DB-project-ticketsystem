# role/Role.py

class Role:
    def __init__(self, cu_id, role):
        self.cu_id = cu_id
        self.role = role

    def is_admin(self):
        return self.role.lower() == 'admin'

    def is_user(self):
        return self.role.lower() == 'user'
