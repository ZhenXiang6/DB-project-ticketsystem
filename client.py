# client.py

import socket
import json

# Server configuration
HOST = '127.0.0.1'
PORT = 8800

def send_request(sock, action, params=None):
    request = {
        "action": action,
        "params": params or {}
    }
    sock.sendall(json.dumps(request).encode('utf-8'))
    response = sock.recv(4096).decode('utf-8')
    return json.loads(response)

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
                        print(response) 
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
        print("[5] Log Out")
        choice = input("---> ").strip()

        if choice == '1':
            e_name = input("Enter Event Name: ").strip()
            c_id = int(input("Enter Category ID: ").strip())
            o_id = int(input("Enter Organizer ID: ").strip())
            e_datetime = input("Enter Event Date and Time (YYYY-MM-DD HH:MM:SS): ").strip()
            e_location = input("Enter Event Location: ").strip()
            description = input("Enter Event Description: ").strip()
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
            e_id = int(input("Enter Event ID: ").strip())
            t_type = input("Enter Ticket Type: ").strip()
            price = float(input("Enter Ticket Price: ").strip())
            total_quantity = int(input("Enter Total Quantity: ").strip())
            response = send_request(sock, 'IssueTickets', {
                'e_id': e_id,
                't_type': t_type,
                'price': price,
                'total_quantity': total_quantity
            })
            print(response.get('message', ''))

        elif choice == '3':
            cu_id = int(input("Enter Customer ID to Query: ").strip())
            response = send_request(sock, 'QueryUserInfo', {'cu_id': cu_id})
            if response['status'] == 'success':
                user_info = response['data']
                for key, value in user_info.items():
                    print(f"{key}: {value}")
            else:
                print(response['message'])

        elif choice == '4':
            cu_id = int(input("Enter Customer ID to Query Purchase History: ").strip())
            response = send_request(sock, 'QueryUserPurchaseHistory', {'cu_id': cu_id})
            if response['status'] == 'success':
                history = response['data']
                for record in history:
                    print(f"Order ID: {record['or_id']}, Event: {record['e_name']}, Ticket Type: {record['t_type']}, Quantity: {record['quantity']}, Subtotal: {record['subtotal']}, Date: {record['or_date']}, Payment Status: {record['payment_status']}")
            else:
                print(response['message'])

        elif choice == '5':
            response = send_request(sock, 'LogOut')
            print(response.get('message', ''))
            break

        else:
            print("Invalid option. Please try again.")


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
            response = send_request(sock, 'BuyTicket', {'e_id': int(e_id), 't_type': t_type, 'quantity': int(quantity)})
            print(response.get('message', ''))

        elif choice == '2':
            or_id = input("Enter Order ID to cancel: ").strip()
            response = send_request(sock, 'CancelTicket', {'or_id': int(or_id)})
            print(response.get('message', ''))

        elif choice == '3':
            e_id = input("Enter Event ID to view details: ").strip()
            response = send_request(sock, 'ViewEventDetails', {'e_id': int(e_id)})
            if response['status'] == 'success':
                data = response['data']
                for key, value in data.items():
                    print(f"{key}: {value}")
            else:
                print(response['message'])

        elif choice == '4':
            response = send_request(sock, 'ListEvent')
            if response['status'] == 'success':
                events = response['data']
                for event in events:
                    print(f"ID: {event['e_id']}, Name: {event['e_name']}, Category: {event['c_name']}, Organizer: {event['o_name']}, Date & Time: {event['e_datetime']}, Location: {event['e_location']}")
            else:
                print(response['message'])

        elif choice == '5':
            search_term = input("Enter search term (Event Name or Organizer): ").strip()
            response = send_request(sock, 'SearchEvent', {'search_term': search_term})
            if response['status'] == 'success':
                events = response['data']
                for event in events:
                    print(f"ID: {event['e_id']}, Name: {event['e_name']}, Category: {event['c_name']}, Organizer: {event['o_name']}, Date & Time: {event['e_datetime']}, Location: {event['e_location']}")
            else:
                print(response['message'])

        elif choice == '6':
            or_id = input("Enter Order ID to make payment: ").strip()
            payment_method = input("Enter Payment Method: ").strip()
            amount = input("Enter Amount: ").strip()
            response = send_request(sock, 'Payment', {'or_id': int(or_id), 'payment_method': payment_method, 'amount': float(amount)})
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
                for record in history:
                    print(f"Order ID: {record['or_id']}, Event: {record['e_name']}, Ticket Type: {record['t_type']}, Quantity: {record['quantity']}, Subtotal: {record['subtotal']}, Date: {record['or_date']}, Payment Status: {record['payment_status']}")
            else:
                print(response['message'])

        elif choice == '9':
            response = send_request(sock, 'LogOut')
            print(response.get('message', ''))
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
