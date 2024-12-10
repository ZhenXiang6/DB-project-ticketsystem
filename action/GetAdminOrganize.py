# action/GetAdminOrganize.py

from DB_utils import get_admin_organization

def get_admin_organize_action(username):
    message = get_admin_organization(username)
    return message

