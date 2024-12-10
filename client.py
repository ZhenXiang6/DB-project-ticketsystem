# client.py

import socket
import json

HOST = '127.0.0.1'
PORT = 8800

def send_json_request(sock, action, params=None):
    request = {
        "action": action,
        "params": params or {}
    }
    data_str = json.dumps(request)
    length_str = str(len(data_str)).encode('utf-8') + b'\n'
    sock.sendall(length_str)
    sock.sendall(data_str.encode('utf-8'))

def recv_json_response(sock):
    # 先讀取長度行
    length_line = b''
    while True:
        ch = sock.recv(1)
        if not ch:
            return None
        if ch == b'\n':
            break
        length_line += ch
    try:
        length = int(length_line.decode('utf-8'))
    except ValueError:
        return None

    # 根據長度讀取JSON
    data = b''
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            return None
        data += chunk
    try:
        return json.loads(data.decode('utf-8'))
    except json.JSONDecodeError:
        return None

def send_request(sock, action, params=None):
    send_json_request(sock, action, params)
    response = recv_json_response(sock)
    if response is None:
        return {"status": "error", "message": "No response from server."}
    return response

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((HOST, PORT))
            print("Connected to the Ticketing System server.\n")
            while True:
                print("----------------------------------------")
                print("Welcome to the Ticketing System! Please select your option:")
                print("[1] Log-in")
                print("[2] Sign-up")
                print("[3] Leave System")
                choice = input("---> ").strip()

                if choice == '1':
                    username = input("Enter username: ").strip()
                    password = input("Enter password: ").strip()
                    response = send_request(sock, 'LogIn', {'username': username, 'password': password})
                    if response['status'] == 'success':
                        print(response['message'])
                        user_role = response.get('role', 'User')
                        print(f"Role: {user_role}")
                        user_menu(sock, user_role)
                    else:
                        print(f"Error: {response['message']}")

                elif choice == '2':
                    username = input("Choose a username: ").strip()
                    password = input("Choose a password: ").strip()
                    email = input("Enter your email: ").strip()
                    response = send_request(sock, 'SignUp', {'username': username, 'password': password, 'email': email})
                    if response['status'] == 'success':
                        print(f"Success: {response['message']}")
                    else:
                        print(f"Error: {response['message']}")

                elif choice == '3':
                    response = send_request(sock, 'Exit')
                    print(response.get('message', 'Exiting...'))
                    break

                else:
                    print("Invalid option. Please try again.")

        except ConnectionRefusedError:
            print("Failed to connect to the server.")
        except KeyboardInterrupt:
            print("\nExiting client.")

def user_menu(sock, role):
    if role.lower() == 'admin':
        admin_menu(sock)
    else:
        regular_user_menu(sock)

def admin_menu(sock):
    while True:
        print("\n----------------------------------------")
        print("Admin Menu - Please select an action:")
        print("[1] Add Event")
        print("[2] Issue Tickets")
        print("[3] Query User Info")
        print("[4] Query User Purchase History")
        print("[5] Generate Sales Report")  # 新增
        print("[6] Log Out")
        choice = input("---> ").strip()

        if choice == '1':
            e_name = input("Enter Event Name: ").strip()
            c_id = input("Enter Category ID: ").strip()
            o_id = input("Enter Organizer ID: ").strip()
            e_datetime = input("Enter Event Date and Time (YYYY-MM-DD HH:MM:SS): ").strip()
            e_location = input("Enter Event Location: ").strip()
            description = input("Enter Event Description: ").strip()
            try:
                c_id = int(c_id)
                o_id = int(o_id)
            except ValueError:
                print("Category ID and Organizer ID must be integers.")
                continue
            response = send_request(sock, 'AddEvent', {
                'e_name': e_name,
                'c_id': c_id,
                'o_id': o_id,
                'e_datetime': e_datetime,
                'e_location': e_location,
                'description': description
            })
            print(response.get('message', ''))

        elif choice == '2':
            e_id = input("Enter Event ID: ").strip()
            t_type = input("Enter Ticket Type: ").strip()
            price = input("Enter Ticket Price: ").strip()
            total_quantity = input("Enter Total Quantity: ").strip()
            try:
                e_id = int(e_id)
                price = float(price)
                total_quantity = int(total_quantity)
            except ValueError:
                print("Event ID and Total Quantity must be integers, and Price must be a number.")
                continue
            response = send_request(sock, 'IssueTickets', {
                'e_id': e_id,
                't_type': t_type,
                'price': price,
                'total_quantity': total_quantity
            })
            print(response.get('message', ''))

        elif choice == '3':
            cu_id = input("Enter Customer ID to Query: ").strip()
            try:
                cu_id = int(cu_id)
            except ValueError:
                print("Customer ID must be an integer.")
                continue
            response = send_request(sock, 'QueryUserInfo', {'cu_id': cu_id})
            if response['status'] == 'success':
                user_info = response['data']
                for key, value in user_info.items():
                    print(f"{key}: {value}")
            else:
                print(response['message'])

        elif choice == '4':
            cu_id = input("Enter Customer ID to Query Purchase History: ").strip()
            try:
                cu_id = int(cu_id)
            except ValueError:
                print("Customer ID must be an integer.")
                continue
            response = send_request(sock, 'QueryUserPurchaseHistory', {'cu_id': cu_id})
            if response['status'] == 'success':
                history = response['data']
                if not history:
                    print("No purchase history found.")
                else:
                    for record in history:
                        print(f"Order ID: {record['or_id']}, Event: {record['e_name']}, "
                              f"Ticket Type: {record['t_type']}, Quantity: {record['quantity']}, "
                              f"Subtotal: {record['subtotal']}, Date: {record['or_date']}, "
                              f"Payment Status: {record['payment_status']}")
            else:
                print(response['message'])

        elif choice == '5':  # 新增
            generate_sales_report(sock)

        elif choice == '6':
            response = send_request(sock, 'LogOut')
            print(response.get('message', ''))
            break

        else:
            print("Invalid option. Please try again.")

def generate_sales_report(sock):
    print("\n--- Generate Sales Report ---")
    event_id = input("Enter Event ID: ").strip()
    try:
        event_id = int(event_id)
    except ValueError:
        print("Event ID must be an integer.")
        return

    response = send_request(sock, 'GenerateSalesReport', {'event_id': event_id})
    if response['status'] == 'success':
        data = response['data']
        print(f"\nSales Report for Event ID: {data['event_id']}")
        print("----------------------------------------")
        print("{:<20} {:<15} {:<15}".format("Ticket Type", "Tickets Sold", "Revenue"))
        print("----------------------------------------")
        for ticket in data['ticket_details']:
            t_type = ticket.get('t_type', 'N/A')
            tickets_sold = ticket.get('tickets_sold', 0)
            revenue = ticket.get('revenue', '0.00')
            print("{:<20} {:<15} {:<15}".format(t_type, tickets_sold, revenue))
        print("----------------------------------------")
        print(f"Total Revenue: {data['total_revenue']}")
    else:
        print(f"Error: {response['message']}")

def regular_user_menu(sock):
    while True:
        print("\n----------------------------------------")
        print("Please select an action:")
        print("[1] Buy Ticket")
        print("[2] Cancel Ticket")
        print("[3] View Event Details")
        print("[4] List Events")
        print("[5] Search Events")
        print("[6] Make Payment")
        print("[7] View/Edit User Info")
        print("[8] View Purchase History")
        print("[9] Log Out")
        choice = input("---> ").strip()

        if choice == '1':
            e_id = input("Enter Event ID: ").strip()
            t_type = input("Enter Ticket Type: ").strip()
            quantity = input("Enter Quantity: ").strip()
            try:
                e_id = int(e_id)
                quantity = int(quantity)
            except ValueError:
                print("Event ID and Quantity must be integers.")
                continue
            response = send_request(sock, 'BuyTicket', {'e_id': e_id, 't_type': t_type, 'quantity': quantity})
            print(response.get('message', ''))

        elif choice == '2':
            or_id = input("Enter Order ID to cancel: ").strip()
            try:
                or_id = int(or_id)
            except ValueError:
                print("Order ID must be an integer.")
                continue
            response = send_request(sock, 'CancelTicket', {'or_id': or_id})
            print(response.get('message', ''))

        elif choice == '3':
            e_id = input("Enter Event ID to view details: ").strip()
            try:
                e_id = int(e_id)
            except ValueError:
                print("Event ID must be an integer.")
                continue
            response = send_request(sock, 'ViewEventDetails', {'e_id': e_id})
            if response['status'] == 'success':
                data = response['data']
                for key, value in data.items():
                    print(f"{key}: {value}")
            else:
                print(response['message'])

        elif choice == '4':
            # Step 1: 請求伺服器傳回所有Category
            response = send_request(sock, 'ListCategories')
            if response['status'] == 'success':
                categories = response['data']
                if not categories:
                    print("No categories found.")
                else:
                    print("Please select a category:")
                    for idx, cat in enumerate(categories, start=1):
                        print(f"[{idx}] {cat['c_name']}")
                    cat_choice = input("---> ").strip()
                    if not cat_choice.isdigit():
                        print("Invalid input.")
                        continue
                    cat_idx = int(cat_choice)
                    if cat_idx < 1 or cat_idx > len(categories):
                        print("Invalid category selection.")
                        continue

                    selected_c_id = categories[cat_idx-1]['c_id']

                    # Step 2: 根據使用者選擇的 c_id 請求該Category下的Events
                    response = send_request(sock, 'ListEventByCategory', {'c_id': selected_c_id})
                    if response['status'] == 'success':
                        events = response['data']
                        if not events:
                            print("No events found in this category.")
                        else:
                            for event in events:
                                print(f"ID: {event['e_id']}, Name: {event['e_name']}, "
                                      f"Category: {event['c_name']}, Organizer: {event['o_name']}, "
                                      f"Date & Time: {event['e_datetime']}, Location: {event['e_location']}")
                    else:
                        print(response['message'])
            else:
                print(response['message'])

        elif choice == '5':
            search_term = input("Enter search term (Event Name or Organizer): ").strip()
            response = send_request(sock, 'SearchEvent', {'search_term': search_term})
            if response['status'] == 'success':
                events = response['data']
                if not events:
                    print("No matching events found.")
                else:
                    for event in events:
                        print(f"ID: {event['e_id']}, Name: {event['e_name']}, "
                              f"Category: {event['c_name']}, Organizer: {event['o_name']}, "
                              f"Date & Time: {event['e_datetime']}, Location: {event['e_location']}")
            else:
                print(response['message'])

        elif choice == '6':
            or_id = input("Enter Order ID to make payment: ").strip()
            payment_method = input("Enter Payment Method: ").strip()
            amount = input("Enter Amount: ").strip()
            try:
                or_id = int(or_id)
                amount = float(amount)
            except ValueError:
                print("Order ID must be an integer and Amount must be a number.")
                continue
            response = send_request(sock, 'Payment', {'or_id': or_id, 'payment_method': payment_method, 'amount': amount})
            print(response.get('message', ''))

        elif choice == '7':
            print("\n--- View/Edit User Info ---")
            print("Select field to edit:")
            print("[1] Username")
            print("[2] Password")
            print("[3] Email")
            print("[4] Phone Number")
            print("[5] Address")
            field_choice = input("---> ").strip()
            field_map = {
                '1': 'cu_name',
                '2': 'pwd',
                '3': 'email',
                '4': 'phone_number',
                '5': 'address'
            }
            field = field_map.get(field_choice)
            if field:
                new_value = input(f"Enter new value for {field}: ").strip()
                response = send_request(sock, 'ViewEditUserInfo', {'field': field, 'new_value': new_value})
                print(response.get('message', ''))
            else:
                print("Invalid field selection.")

        elif choice == '8':
            response = send_request(sock, 'ViewPurchaseHistory')
            if response['status'] == 'success':
                history = response['data']
                if not history:
                    print("No purchase history found.")
                else:
                    for record in history:
                        print(f"Order ID: {record['or_id']}, Event: {record['e_name']}, "
                              f"Ticket Type: {record['t_type']}, Quantity: {record['quantity']}, "
                              f"Subtotal: {record['subtotal']}, Date: {record['or_date']}, "
                              f"Payment Status: {record['payment_status']}")
            else:
                print(response['message'])

        elif choice == '9':
            response = send_request(sock, 'LogOut')
            print(response.get('message', ''))
            break

        else:
            print("Invalid option. Please try again.")

def generate_sales_report(sock):
    print("\n--- Generate Sales Report ---")
    event_id = input("Enter Event ID: ").strip()
    try:
        event_id = int(event_id)
    except ValueError:
        print("Event ID must be an integer.")
        return

    response = send_request(sock, 'GenerateSalesReport', {'event_id': event_id})
    if response['status'] == 'success':
        data = response['data']
        print(f"\nSales Report for Event ID: {data['event_id']}")
        print("----------------------------------------")
        print("{:<20} {:<15} {:<15}".format("Ticket Type", "Tickets Sold", "Revenue"))
        print("----------------------------------------")
        for ticket in data['ticket_details']:
            t_type = ticket.get('t_type', 'N/A')
            tickets_sold = ticket.get('tickets_sold', 0)
            revenue = ticket.get('revenue', '0.00')
            print("{:<20} {:<15} {:<15}".format(t_type, tickets_sold, revenue))
        print("----------------------------------------")
        print(f"Total Revenue: {data['total_revenue']}")
    else:
        print(f"Error: {response['message']}")

if __name__ == "__main__":
    main()
