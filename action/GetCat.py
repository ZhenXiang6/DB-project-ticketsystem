# action/GetCat.py


from DB_utils import get_categories

def get_categories_action():
    data, message = get_categories()
    return data, message