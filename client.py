# client.py

import socket

def receive_message(conn):
    try:
        message = conn.recv(4096).decode('utf-8')
        if not message:
            return None
        return message
    except Exception as e:
        print(f"Receive message error: {e}")
        return None

def main():
    conn_ip = "127.0.0.1"
    conn_port = 8800

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    try:
        client_socket.connect((conn_ip, conn_port))
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        return

    try:
        while True:
            recv_msg = receive_message(client_socket)
            if recv_msg is None:
                print("Connection closed by the server.")
                break

            if "[EXIT]" in recv_msg:
                print(recv_msg.replace("[EXIT]", '').strip())
                break

            if "[TABLE]" in recv_msg:
                table = recv_msg.replace("[TABLE]", '').replace("[END]", '').strip()
                print(table)

            elif "[INPUT]" in recv_msg:
                prompt = recv_msg.replace("[INPUT]", '').strip()
                user_input = input(prompt)
                client_socket.send(user_input.encode('utf-8'))

            else:
                print(recv_msg, end='')
    except KeyboardInterrupt:
        print("\nExiting the client.")
    finally:
        client_socket.close()

if __name__ == '__main__':
    main()
