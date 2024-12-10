# action/CustomerDetail.py

from DB_utils import customer_detail

def get_customer_detail_action(cu_name):
    detail = customer_detail(cu_name)
    return detail
