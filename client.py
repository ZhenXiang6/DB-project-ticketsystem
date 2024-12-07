# client.py

import socket

# 設置伺服器參數
HOST = '127.0.0.1'  # 伺服器的主機地址
PORT = 8800         # 伺服器的端口

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("Connected to the Ticketing System server.")
        except ConnectionRefusedError:
            print("Failed to connect to the server. Ensure that the server is running.")
            return

        while True:
            try:
                # 接收伺服器發送的訊息
                data = s.recv(4096)
                if not data:
                    print("Disconnected from server.")
                    break
                print(data.decode(), end='')

                # 根據伺服器提示進行輸入
                user_input = input()
                s.sendall(user_input.encode())
            except KeyboardInterrupt:
                print("\nExiting the system. Goodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

if __name__ == "__main__":
    main()
