# action/payment/Payment.py

from DB_utils import payment_processing

def payment_action(or_id, payment_method, amount):
    success, message = payment_processing(or_id, payment_method, amount)
    return success, message
