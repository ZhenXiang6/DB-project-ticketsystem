import socket
import threading
import json
from datetime import datetime
from decimal import Decimal
from role import Admin, User
import logging
from action import (
    signup_action,
    login_action,
    exit_action,
    add_event_action,
    issue_tickets_action,
    query_user_info_action,
    query_user_purchase_history_action,
    buy_ticket_action,
    cancel_ticket_action,
    view_event_details_action,
    list_event_action,
    search_event_action,
    payment_action,
    view_edit_user_info_action,
    view_purchase_history_action,
    list_history_action
)
from utils import format_response, serialize_datetimes
from DB_utils import db

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

HOST = '127.0.0.1'
PORT = 8800
connected_users = {}

class DateTimeDecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return str(obj)  # 使用 str 保持精度
        return super().default(obj)


def send_json_response(client_socket, response):
    # 將 response 轉為 JSON 字串
    serialized = json.dumps(response, cls=DateTimeDecimalEncoder)
    # 傳送長度 + '\n'
    length_str = str(len(serialized)).encode('utf-8') + b'\n'
    client_socket.sendall(length_str)
    # 傳送實際 JSON
    client_socket.sendall(serialized.encode('utf-8'))

def recv_json_request(client_socket):
    # 先讀取長度行
    length_line = b''
    while True:
        ch = client_socket.recv(1)
        if not ch:
            return None
        if ch == b'\n':
            break
        length_line += ch
    length = int(length_line.decode('utf-8'))
    # 根據長度讀取完整 JSON
    data = b''
    while len(data) < length:
        chunk = client_socket.recv(length - len(data))
        if not chunk:
            return None
        data += chunk
    return json.loads(data.decode('utf-8'))


def handle_client(client_socket, address):
    logging.info(f"Accepted connection from {address}")
    user = None
    while True:
        try:
            request = recv_json_request(client_socket)
            if request is None:
                break
            action = request.get('action')
            params = request.get('params', {})
            response = {}

            if action == 'SignUp':
                username = params.get('username')
                password = params.get('password')
                email = params.get('email')
                success, message = signup_action(username, password, email)
                if success:
                    response = {"status": "success", "message": message}
                else:
                    response = {"status": "error", "message": message}

            elif action == 'LogIn':
                username = params.get('username')
                password = params.get('password')
                success, result = login_action(username, password)
                if success:
                    cu_id = result['cu_id']
                    role = result['role']
                    if role.lower() == 'admin':
                        user = Admin(cu_id, role)
                    else:
                        user = User(cu_id, role)
                    connected_users[client_socket] = user
                    response = {"status": "success", "message": f"Logged in as {role}.", "role": role}
                else:
                    response = {"status": "error", "message": result}

            elif action == 'LogOut':
                if client_socket in connected_users:
                    user = connected_users.pop(client_socket)
                    response = {"status": "success", "message": "Logged out successfully."}
                else:
                    response = {"status": "error", "message": "You are not logged in."}

            elif action == 'AddEvent':
                if isinstance(user, Admin):
                    e_name = params.get('e_name')
                    c_id = params.get('c_id')
                    o_id = params.get('o_id')
                    e_datetime = params.get('e_datetime')
                    e_location = params.get('e_location')
                    description = params.get('description')
                    event_id, message = user.add_event(e_name, c_id, o_id, e_datetime, e_location, description)
                    if event_id:
                        response = {"status": "success", "message": message, "e_id": event_id}
                    else:
                        response = {"status": "error", "message": message}
                else:
                    response = {"status": "error", "message": "Unauthorized action. Admins only."}

            elif action == 'IssueTickets':
                if isinstance(user, Admin):
                    e_id = params.get('e_id')
                    t_type = params.get('t_type')
                    price = params.get('price')
                    total_quantity = params.get('total_quantity')
                    success, message = user.issue_tickets(e_id, t_type, price, total_quantity)
                    if success:
                        response = {"status": "success", "message": message}
                    else:
                        response = {"status": "error", "message": message}
                else:
                    response = {"status": "error", "message": "Unauthorized action. Admins only."}

            elif action == 'QueryUserInfo':
                if isinstance(user, Admin):
                    cu_id = params.get('cu_id')
                    user_info = user.query_user_info(cu_id)
                    if user_info:
                        user_info = serialize_datetimes(user_info)
                        response = {"status": "success", "data": user_info}
                    else:
                        response = {"status": "error", "message": "User not found."}
                else:
                    response = {"status": "error", "message": "Unauthorized action. Admins only."}

            elif action == 'QueryUserPurchaseHistory':
                if isinstance(user, Admin):
                    cu_id = params.get('cu_id')
                    history = user.query_user_purchase_history(cu_id)
                    if history:
                        history = serialize_datetimes(history)
                        response = {"status": "success", "data": history}
                    else:
                        response = {"status": "error", "message": "Purchase history not found."}
                else:
                    response = {"status": "error", "message": "Unauthorized action. Admins only."}

            elif action == 'BuyTicket':
                if isinstance(user, User):
                    e_id = params.get('e_id')
                    t_type = params.get('t_type')
                    quantity = params.get('quantity')
                    cu_id = user.cu_id
                    success, message = buy_ticket_action(e_id, t_type, quantity, cu_id)
                    if success:
                        response = {"status": "success", "message": message}
                    else:
                        response = {"status": "error", "message": message}
                else:
                    response = {"status": "error", "message": "Please log in as a user."}

            elif action == 'CancelTicket':
                if isinstance(user, User):
                    or_id = params.get('or_id')
                    success, message = cancel_ticket_action(or_id, user.cu_id)
                    if success:
                        response = {"status": "success", "message": message}
                    else:
                        response = {"status": "error", "message": message}
                else:
                    response = {"status": "error", "message": "Please log in as a user."}

            elif action == 'ViewEventDetails':
                e_id = params.get('e_id')
                if user:
                    details = user.view_event_details(e_id)
                else:
                    details = view_event_details_action(e_id)
                if details:
                    details = serialize_datetimes(details)
                    response = {"status": "success", "data": details}
                else:
                    response = {"status": "error", "message": "Event not found."}

            elif action == 'ListEvent':
                if user and isinstance(user, User):
                    events = user.list_events()
                else:
                    events = list_event_action()
                if events:
                    events = serialize_datetimes(events)
                    response = {"status": "success", "data": events}
                else:
                    response = {"status": "error", "message": "No events found."}

            elif action == 'SearchEvent':
                search_term = params.get('search_term')
                if user and isinstance(user, User):
                    events = user.search_event(search_term)
                else:
                    events = search_event_action(search_term)
                if events:
                    events = serialize_datetimes(events)
                    response = {"status": "success", "data": events}
                else:
                    response = {"status": "error", "message": "No matching events found."}

            elif action == 'Payment':
                if isinstance(user, User):
                    or_id = params.get('or_id')
                    payment_method = params.get('payment_method')
                    amount = params.get('amount')
                    success, message = payment_action(or_id, payment_method, amount)
                    if success:
                        response = {"status": "success", "message": message}
                    else:
                        response = {"status": "error", "message": message}
                else:
                    response = {"status": "error", "message": "Please log in as a user."}

            elif action == 'ViewEditUserInfo':
                if isinstance(user, User):
                    field = params.get('field')
                    new_value = params.get('new_value')
                    success, message = view_edit_user_info_action(user.cu_id, field, new_value)
                    if success:
                        response = {"status": "success", "message": message}
                    else:
                        response = {"status": "error", "message": message}
                else:
                    response = {"status": "error", "message": "Please log in as a user."}

            elif action == 'ViewPurchaseHistory':
                if isinstance(user, User):
                    history = user.view_purchase_history()
                    if history:
                        history = serialize_datetimes(history)
                        response = {"status": "success", "data": history}
                    else:
                        response = {"status": "error", "message": "No purchase history found."}
                else:
                    response = {"status": "error", "message": "Please log in as a user."}

            elif action == 'ListHistory':
                if isinstance(user, User):
                    history = list_history_action(user.cu_id)
                    if history:
                        history = serialize_datetimes(history)
                        response = {"status": "success", "data": history}
                    else:
                        response = {"status": "error", "message": "No history found."}
                else:
                    response = {"status": "error", "message": "Please log in as a user."}

            elif action == 'Exit':
                message = exit_action()
                response = {"status": "success", "message": message}
                send_json_response(client_socket, response)
                break

            else:
                response = {"status": "error", "message": "Invalid action."}

            send_json_response(client_socket, response)

        except Exception as e:
            logging.error(f"Error handling client {address}: {e}")
            response = {"status": "error", "message": "An error occurred on the server."}
            send_json_response(client_socket, response)
            break

    logging.info(f"Connection closed from {address}")
    if client_socket in connected_users:
        connected_users.pop(client_socket)
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    logging.info(f"Server listening on {HOST}:{PORT}...")
    try:
        while True:
            client_socket, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
    except KeyboardInterrupt:
        logging.info("Shutting down server.")
    finally:
        server.close()
        db.close()

if __name__ == "__main__":
    start_server()
