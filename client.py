import socket
from os.path import isfile, getsize

conn_ip = "127.0.0.1"
conn_port = 8800

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
client_socket.connect((conn_ip, conn_port))


def receive_message(conn):
    try:
        message = b""
        first_chunk = conn.recv(4096)
        if "[TABLE]".encode('utf-8') not in first_chunk:
            return first_chunk.decode('utf-8')
        
        message += first_chunk

        while True:
            chunk = conn.recv(4096)
            if not chunk:
                raise ConnectionError("Connection lost while receiving data")
            message += chunk
            if "[END]".encode('utf-8') in message:
                break
        return message.decode('utf-8').replace("[END]", '').replace("[TABLE]", '')
    except Exception:
        print("Receive message error.")
        return

try: 
    while True:  # Keep receiving and sending message with server
        
        recv_msg = receive_message(client_socket)
        if not recv_msg:
            print("Connection closed by the server.")
            break
        if recv_msg.find("[EXIT]") != -1:
            print(recv_msg.replace("[EXIT]", ''), end='')
            break
        if recv_msg.find("[TABLE]") != -1:
            print(recv_msg.replace("[TABLE]", '').replace("[END]", ''), end='')
            # Optional: Implement table parsing/display

        elif recv_msg.find("[INPUT]") != -1:
            print(recv_msg.replace("[INPUT]", ''), end='')

            send_msg = input().strip()
            while len(send_msg) == 0:
                print("Input cannot be empty. Please enter again:", end=' ')
                send_msg = input().strip()

            if send_msg.lower() == "exit":
                break            
            client_socket.send(send_msg.encode('utf-8'))

        else:
            print(recv_msg, end='')
        
finally:
    print("Connection closed.")
    client_socket.close()
