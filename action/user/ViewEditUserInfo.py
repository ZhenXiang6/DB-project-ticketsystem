# action/user/ViewEditUserInfo.py
from ..Action import Action
from DB_utils import get_user_info, update_user_info

class ViewEditUserInfo(Action):
    def exec(self, conn, user):
        # 查看用戶資訊
        user_info = get_user_info(user.get_userid())
        self.send_table(conn, user_info)
        
        # 提供編輯選項
        conn.send("Do you want to edit your information? (yes/no): ".encode('utf-8'))
        response = conn.recv(100).decode('utf-8').strip().lower()
        if response != 'yes':
            return
        
        # 選擇要編輯的項目
        editable_fields = ["Name", "Email", "Phone Number", "Address"]
        msg = "Select the field you want to edit:\n"
        for idx, field in enumerate(editable_fields, 1):
            msg += f"[{idx}] {field}\n"
        conn.send(f'[INPUT]{msg}---> '.encode('utf-8'))
        selection_str = conn.recv(100).decode('utf-8').strip()
        if not selection_str.isdigit() or not (1 <= int(selection_str) <= len(editable_fields)):
            conn.send("Invalid selection.\n".encode('utf-8'))
            return
        selection = int(selection_str)
        field = editable_fields[selection - 1]
        
        # 輸入新的值
        new_value = self.read_input(conn, f"new {field.lower()}")
        if field == "Name":
            field_db = "cu_name"
        elif field == "Email":
            field_db = "email"
        elif field == "Phone Number":
            field_db = "phone_number"
        elif field == "Address":
            field_db = "address"
        
        # 更新資料庫
        success, message = update_user_info(user.get_userid(), field_db, new_value)
        conn.send(f"{message}\n".encode('utf-8'))
