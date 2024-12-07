# server.py

import socket
import threading
from DB_utils import (
    authenticate_user,
    register_user,
    list_available_events,
    get_event_details,
    list_ticket_types,
    purchase_ticket,
    list_user_purchases_history,
    list_pending_orders,
    process_payment,
    view_edit_user_info,
    list_user_purchases,
    list_categories,
    list_organizers,
    add_event,
    issue_ticket,
    search_events,
    get_user_role,
    db_connect
)
from tabulate import tabulate

# 設置伺服器參數
HOST = '127.0.0.1'  # 本地主機
PORT = 8800         # 監聽端口

# 建立鎖以同步資料庫操作（如果需要）
db_lock = threading.Lock()

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    session = db_connect()
    current_user_id = None
    user_role = None

    try:
        while True:
            conn.sendall(b"\n----------------------------------------\n")
            if not current_user_id:
                conn.sendall(b"Welcome to the Ticketing System! Please select your option:\n")
                conn.sendall(b"[1] Log-in\n[2] Sign-up\n[3] Leave System\n---> ")
                option = conn.recv(1024).decode().strip()

                if option == '1':
                    conn.sendall(b"Please enter username: ")
                    username = conn.recv(1024).decode().strip()
                    conn.sendall(b"Please enter password: ")
                    password = conn.recv(1024).decode().strip()

                    with db_lock:
                        user_id, role = authenticate_user(username, password)
                    
                    if user_id:
                        current_user_id = user_id
                        user_role = role
                        conn.sendall(f"\n----------------------------------------\n\nHi {username}!\n[ User Info ] User ID: {user_id}, Username: {username}, Role: {role}\n".encode())
                    else:
                        conn.sendall(b"Invalid username or password.\n")
                
                elif option == '2':
                    conn.sendall(b"Please enter new username: ")
                    username = conn.recv(1024).decode().strip()
                    conn.sendall(b"Please enter new password: ")
                    password = conn.recv(1024).decode().strip()
                    conn.sendall(b"Please enter email: ")
                    email = conn.recv(1024).decode().strip()

                    with db_lock:
                        user_id = register_user(username, password, email)
                    
                    if user_id:
                        conn.sendall(f"User registered successfully with User ID: {user_id}\n".encode())
                    else:
                        conn.sendall(b"Registration failed. Username might already exist.\n")
                
                elif option == '3':
                    conn.sendall(b"Exiting the system. Goodbye!\n")
                    break
                else:
                    conn.sendall(b"Invalid option. Please try again.\n")
            
            else:
                # 用戶已登入，顯示功能選項
                if user_role == 'Admin':
                    conn.sendall(b"\nPlease select an option:\n")
                    conn.sendall(b"[1] List All Available Events\n[2] View Event Details\n[3] Purchase Ticket\n[4] Cancel Ticket\n[5] Payment\n[6] View Purchase History\n[7] View/Edit User Information\n[8] Admin: Add Event\n[9] Admin: Issue Ticket\n[10] Admin: Query User Information\n[11] Admin: Query User Purchase History\n[12] Logout\n[13] Exit\n---> ")
                else:
                    conn.sendall(b"\nPlease select an option:\n")
                    conn.sendall(b"[1] List All Available Events\n[2] View Event Details\n[3] Purchase Ticket\n[4] Cancel Ticket\n[5] Payment\n[6] View Purchase History\n[7] View/Edit User Information\n[8] Logout\n[9] Exit\n---> ")

                option = conn.recv(1024).decode().strip()

                if user_role == 'Admin':
                    if option == '1':
                        events = list_available_events()
                        conn.sendall(f"{events}\n".encode())
                    
                    elif option == '2':
                        conn.sendall(b"Please enter event ID: ")
                        event_id = conn.recv(1024).decode().strip()
                        details = get_event_details(event_id)
                        conn.sendall(f"{details}\n".encode())
                    
                    elif option == '3':
                        conn.sendall(b"Please enter event ID to purchase ticket: ")
                        event_id = conn.recv(1024).decode().strip()
                        conn.sendall(b"Please enter ticket type (e.g., VIP, Regular): ")
                        ticket_type = conn.recv(1024).decode().strip()
                        conn.sendall(b"Please enter quantity: ")
                        quantity = conn.recv(1024).decode().strip()

                        with db_lock:
                            success, message = purchase_ticket(current_user_id, event_id, ticket_type, int(quantity))
                        
                        conn.sendall(f"{message}\n".encode())
                    
                    elif option == '4':
                        # Cancel ticket functionality to be implemented
                        conn.sendall(b"Cancel Ticket functionality not implemented yet.\n")
                    
                    elif option == '5':
                        pending_orders = list_pending_orders(current_user_id)
                        conn.sendall(f"{pending_orders}\n".encode())
                        conn.sendall(b"Please enter Order ID to make payment: ")
                        or_id = conn.recv(1024).decode().strip()
                        conn.sendall(b"Please enter Payment Method (e.g., Credit Card, PayPal): ")
                        payment_method = conn.recv(1024).decode().strip()

                        with db_lock:
                            success, message = process_payment(current_user_id, or_id, payment_method)
                        
                        conn.sendall(f"{message}\n".encode())
                    
                    elif option == '6':
                        history = list_user_purchases_history(current_user_id)
                        conn.sendall(f"{history}\n".encode())
                    
                    elif option == '7':
                        conn.sendall(b"Select field to edit:\n")
                        conn.sendall(b"[1] Username\n[2] Password\n[3] Email\n[4] Phone Number\n[5] Address\n---> ")
                        field_option = conn.recv(1024).decode().strip()
                        fields = {
                            '1': 'cu_name',
                            '2': 'password',
                            '3': 'email',
                            '4': 'phone_number',
                            '5': 'address'
                        }
                        field = fields.get(field_option, None)
                        if field:
                            conn.sendall(f"Please enter new value for {field.replace('_', ' ').title()}: ".encode())
                            new_value = conn.recv(1024).decode().strip()
                            with db_lock:
                                success, message = view_edit_user_info(current_user_id, field, new_value)
                            conn.sendall(f"{message}\n".encode())
                        else:
                            conn.sendall(b"Invalid field selection.\n")
                    
                    elif option == '8':
                        # Admin: Add Event
                        conn.sendall(b"Please enter event name: ")
                        e_name = conn.recv(1024).decode().strip()
                        conn.sendall(b"Please enter category ID: ")
                        c_id = conn.recv(1024).decode().strip()
                        conn.sendall(b"Please enter organizer ID: ")
                        o_id = conn.recv(1024).decode().strip()
                        conn.sendall(b"Please enter event date and time (YYYY-MM-DD HH:MM:SS): ")
                        e_datetime = conn.recv(1024).decode().strip()
                        conn.sendall(b"Please enter event location: ")
                        e_location = conn.recv(1024).decode().strip()
                        conn.sendall(b"Please enter event description: ")
                        description = conn.recv(1024).decode().strip()

                        with db_lock:
                            success, message = add_event(e_name, int(c_id), int(o_id), e_datetime, e_location, description)
                        
                        conn.sendall(f"{message}\n".encode())
                    
                    elif option == '9':
                        # Admin: Issue Ticket
                        conn.sendall(b"Please enter event ID: ")
                        e_id = conn.recv(1024).decode().strip()
                        conn.sendall(b"Please enter ticket type (e.g., VIP, Regular): ")
                        t_type = conn.recv(1024).decode().strip()
                        conn.sendall(b"Please enter ticket price: ")
                        price = conn.recv(1024).decode().strip()
                        conn.sendall(b"Please enter total quantity: ")
                        total_quantity = conn.recv(1024).decode().strip()

                        with db_lock:
                            success, message = issue_ticket(int(e_id), t_type, float(price), int(total_quantity))
                        
                        conn.sendall(f"{message}\n".encode())
                    
                    elif option == '10':
                        # Admin: Query User Information
                        conn.sendall(b"Please enter username to query: ")
                        username = conn.recv(1024).decode().strip()
                        user = session.query(Customer).filter_by(cu_name=username).first()
                        if user:
                            data = [[
                                user.cu_id,
                                user.cu_name,
                                user.email,
                                user.role
                            ]]
                            headers = ["User ID", "Username", "Email", "Role"]
                            user_info = tabulate(data, headers=headers, tablefmt="github")
                            conn.sendall(f"{user_info}\n".encode())
                        else:
                            conn.sendall(b"User not found.\n")
                    
                    elif option == '11':
                        # Admin: Query User Purchase History
                        conn.sendall(b"Please enter username to query purchase history: ")
                        username = conn.recv(1024).decode().strip()
                        user = session.query(Customer).filter_by(cu_name=username).first()
                        if user:
                            history = list_user_purchases_history(user.cu_id)
                            conn.sendall(f"{history}\n".encode())
                        else:
                            conn.sendall(b"User not found.\n")
                    
                    elif option == '12':
                        # Logout
                        current_user_id = None
                        user_role = None
                        conn.sendall(b"You have been logged out successfully.\n")
                    
                    elif option == '13':
                        conn.sendall(b"Exiting the system. Goodbye!\n")
                        break
                    
                    else:
                        conn.sendall(b"Invalid option. Please try again.\n")
                
                else:
                    # 一般用戶功能
                    if option == '1':
                        events = list_available_events()
                        conn.sendall(f"{events}\n".encode())
                    
                    elif option == '2':
                        conn.sendall(b"Please enter event ID: ")
                        event_id = conn.recv(1024).decode().strip()
                        details = get_event_details(event_id)
                        conn.sendall(f"{details}\n".encode())
                    
                    elif option == '3':
                        conn.sendall(b"Please enter event ID to purchase ticket: ")
                        event_id = conn.recv(1024).decode().strip()
                        conn.sendall(b"Please enter ticket type (e.g., VIP, Regular): ")
                        ticket_type = conn.recv(1024).decode().strip()
                        conn.sendall(b"Please enter quantity: ")
                        quantity = conn.recv(1024).decode().strip()

                        with db_lock:
                            success, message = purchase_ticket(current_user_id, event_id, ticket_type, int(quantity))
                        
                        conn.sendall(f"{message}\n".encode())
                    
                    elif option == '4':
                        # Cancel ticket functionality to be implemented
                        conn.sendall(b"Cancel Ticket functionality not implemented yet.\n")
                    
                    elif option == '5':
                        pending_orders = list_pending_orders(current_user_id)
                        conn.sendall(f"{pending_orders}\n".encode())
                        conn.sendall(b"Please enter Order ID to make payment: ")
                        or_id = conn.recv(1024).decode().strip()
                        conn.sendall(b"Please enter Payment Method (e.g., Credit Card, PayPal): ")
                        payment_method = conn.recv(1024).decode().strip()

                        with db_lock:
                            success, message = process_payment(current_user_id, or_id, payment_method)
                        
                        conn.sendall(f"{message}\n".encode())
                    
                    elif option == '6':
                        history = list_user_purchases_history(current_user_id)
                        conn.sendall(f"{history}\n".encode())
                    
                    elif option == '7':
                        conn.sendall(b"Select field to edit:\n")
                        conn.sendall(b"[1] Username\n[2] Password\n[3] Email\n[4] Phone Number\n[5] Address\n---> ")
                        field_option = conn.recv(1024).decode().strip()
                        fields = {
                            '1': 'cu_name',
                            '2': 'password',
                            '3': 'email',
                            '4': 'phone_number',
                            '5': 'address'
                        }
                        field = fields.get(field_option, None)
                        if field:
                            conn.sendall(f"Please enter new value for {field.replace('_', ' ').title()}: ".encode())
                            new_value = conn.recv(1024).decode().strip()
                            with db_lock:
                                success, message = view_edit_user_info(current_user_id, field, new_value)
                            conn.sendall(f"{message}\n".encode())
                        else:
                            conn.sendall(b"Invalid field selection.\n")
                    
                    elif option == '8':
                        # Logout
                        current_user_id = None
                        user_role = None
                        conn.sendall(b"You have been logged out successfully.\n")
                    
                    elif option == '9':
                        conn.sendall(b"Exiting the system. Goodbye!\n")
                        break
                    
                    else:
                        conn.sendall(b"Invalid option. Please try again.\n")
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")

def start_server():
    """
    啟動伺服器並開始監聽連接
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT} ...")
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    start_server()
