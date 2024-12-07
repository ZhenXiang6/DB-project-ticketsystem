# action/Action.py

class Action:
    def __init__(self, action_name):
        self.action_name = action_name

    def exec(self, conn, user=None):
        raise NotImplementedError("Subclasses should implement this!")

    def get_name(self):
        return self.action_name

    def read_input(self, conn, prompt):
        conn.send(f'[INPUT]Please enter {prompt}: '.encode('utf-8'))
        recv_msg = conn.recv(1024).decode('utf-8').strip()
        return recv_msg

    def send_table(self, conn, table):
        # 使用 [TABLE] 和 [END] 標籤來傳輸長訊息
        message = f'[TABLE]\n{table}\n[END]'
        conn.sendall(message.encode('utf-8'))
