# DB_utils.py

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import sys
from datetime import datetime

class Database:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        try:
            self.connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        except Exception as e:
            print(f"Failed to connect to the database: {e}")
            sys.exit(1)

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            if self.cursor.description:
                return self.cursor.fetchall()
        except Exception as e:
            print(f"Database query error: {e}")
            return None

    def close(self):
        self.cursor.close()
        self.connection.close()

# 初始化資料庫連接
# 請根據您的資料庫設定修改以下參數
db = Database(
    dbname='ticketsystem',
    user='postgres',
    password='your_password',  # 替換為您的密碼
    host='localhost',
    port=5432
)

# 資料庫工具函數

def authenticate_user(username, password):
    query = """
    SELECT cu_id, role FROM CUSTOMER WHERE cu_name = %s AND pwd = %s;
    """
    result = db.execute_query(query, (username, password))
    if result:
        return result[0]['cu_id'], result[0]['role']
    return None, None

def register_user(username, password, email):
    if username_exists(username):
        return None, "Username already exists."
    if email_exists(email):
        return None, "Email already exists."
    query = """
    INSERT INTO CUSTOMER (cu_name, pwd, email) VALUES (%s, %s, %s) RETURNING cu_id;
    """
    result = db.execute_query(query, (username, password, email))
    if result:
        return result[0]['cu_id'], "User registered successfully."
    return None, "Registration failed."

def username_exists(username):
    query = """
    SELECT 1 FROM CUSTOMER WHERE cu_name = %s;
    """
    result = db.execute_query(query, (username,))
    return bool(result)

def email_exists(email):
    query = """
    SELECT 1 FROM CUSTOMER WHERE email = %s;
    """
    result = db.execute_query(query, (email,))
    return bool(result)

def add_event(e_name, c_id, o_id, e_datetime, e_location, description):
    query = """
    INSERT INTO EVENT (e_name, c_id, o_id, e_datetime, e_location, description)
    VALUES (%s, %s, %s, %s, %s, %s) RETURNING e_id;
    """
    result = db.execute_query(query, (e_name, c_id, o_id, e_datetime, e_location, description))
    if result:
        return result[0]['e_id'], "Event added successfully."
    return None, "Failed to add event."

def issue_ticket(e_id, t_type, price, total_quantity):
    # 檢查活動是否存在
    query = "SELECT 1 FROM EVENT WHERE e_id = %s;"
    if not db.execute_query(query, (e_id,)):
        return False, "Event does not exist."
    # 檢查票種是否已存在
    query = "SELECT 1 FROM TICKET WHERE e_id = %s AND t_type = %s;"
    if db.execute_query(query, (e_id, t_type)):
        return False, "Ticket type already exists for this event."
    # 插入票種
    query = """
    INSERT INTO TICKET (e_id, t_type, price, total_quantity, remain_quantity)
    VALUES (%s, %s, %s, %s, %s) RETURNING t_id;
    """
    result = db.execute_query(query, (e_id, t_type, price, total_quantity, total_quantity))
    if result:
        return True, "Ticket issued successfully."
    return False, "Failed to issue ticket."

def query_user_info(cu_id):
    query = """
    SELECT cu_id, cu_name, email, phone_number, address, role FROM CUSTOMER WHERE cu_id = %s;
    """
    result = db.execute_query(query, (cu_id,))
    if result:
        return result[0]
    return None

def query_user_purchase_history(cu_id):
    query = """
    SELECT O.or_id, E.e_name, T.t_type, OD.quantity, OD.subtotal, O.or_date, O.payment_status
    FROM "ORDER" O
    JOIN ORDER_DETAIL OD ON O.or_id = OD.or_id
    JOIN TICKET T ON OD.t_id = T.t_id
    JOIN EVENT E ON T.e_id = E.e_id
    WHERE O.cu_id = %s
    ORDER BY O.or_date DESC;
    """
    result = db.execute_query(query, (cu_id,))
    return result if result else []

def buy_ticket(cu_id, e_id, t_type, quantity):
    try:
        db.cursor.execute("BEGIN;")
        # 取得票券並加鎖以避免並發問題
        query = """
        SELECT t_id, price, remain_quantity FROM TICKET
        WHERE e_id = %s AND t_type = %s FOR UPDATE;
        """
        result = db.execute_query(query, (e_id, t_type))
        if not result:
            db.cursor.execute("ROLLBACK;")
            return False, "Ticket type or event does not exist."
        ticket = result[0]
        if ticket['remain_quantity'] < quantity:
            db.cursor.execute("ROLLBACK;")
            return False, f"Only {ticket['remain_quantity']} tickets available."
        # 更新剩餘數量
        new_remain = ticket['remain_quantity'] - quantity
        query = "UPDATE TICKET SET remain_quantity = %s WHERE t_id = %s;"
        db.execute_query(query, (new_remain, ticket['t_id']))
        # 插入訂單
        total_amount = float(ticket['price']) * quantity
        query = """
        INSERT INTO "ORDER" (cu_id, or_date, total_amount, payment_status, is_canceled)
        VALUES (%s, %s, %s, 'Pending', FALSE) RETURNING or_id;
        """
        result = db.execute_query(query, (cu_id, datetime.now(), total_amount))
        if not result:
            db.cursor.execute("ROLLBACK;")
            return False, "Failed to create order."
        or_id = result[0]['or_id']
        # 插入訂單明細
        query = """
        INSERT INTO ORDER_DETAIL (or_id, t_id, quantity, subtotal)
        VALUES (%s, %s, %s, %s);
        """
        db.execute_query(query, (or_id, ticket['t_id'], quantity, total_amount))
        # 提交交易
        db.cursor.execute("COMMIT;")
        return True, f"Successfully purchased {quantity} ticket(s) for event {e_id}."
    except Exception as e:
        db.cursor.execute("ROLLBACK;")
        print(f"Buy ticket error: {e}")
        return False, "Failed to purchase ticket."

def cancel_ticket(or_id, cu_id):
    # 更新訂單為已取消，並恢復票券數量
    try:
        db.cursor.execute("BEGIN;")
        # 檢查訂單是否存在且可取消
        query = """
        SELECT payment_status, is_canceled FROM "ORDER" WHERE or_id = %s AND cu_id = %s;
        """
        result = db.execute_query(query, (or_id, cu_id))
        if not result:
            db.cursor.execute("ROLLBACK;")
            return False, "Order does not exist."
        order = result[0]
        if order['is_canceled'] or order['payment_status'] != 'Pending':
            db.cursor.execute("ROLLBACK;")
            return False, "Cannot cancel this order."
        # 更新訂單狀態
        query = """
        UPDATE "ORDER" SET is_canceled = TRUE, payment_status = 'Canceled' WHERE or_id = %s;
        """
        db.execute_query(query, (or_id,))
        # 恢復票券數量
        query = """
        SELECT t_id, quantity FROM ORDER_DETAIL WHERE or_id = %s;
        """
        details = db.execute_query(query, (or_id,))
        for detail in details:
            query = "UPDATE TICKET SET remain_quantity = remain_quantity + %s WHERE t_id = %s;"
            db.execute_query(query, (detail['quantity'], detail['t_id']))
        db.cursor.execute("COMMIT;")
        return True, "Order canceled successfully."
    except Exception as e:
        db.cursor.execute("ROLLBACK;")
        print(f"Cancel ticket error: {e}")
        return False, "Failed to cancel order."

def view_event_details(e_id):
    query = """
    SELECT E.e_id, E.e_name, C.c_name, O.o_name, E.e_datetime, E.e_location, E.description
    FROM EVENT E
    JOIN CATEGORY C ON E.c_id = C.c_id
    JOIN ORGANIZER O ON E.o_id = O.o_id
    WHERE E.e_id = %s;
    """
    result = db.execute_query(query, (e_id,))
    if result:
        return result[0]
    return None

def list_events():
    query = """
    SELECT E.e_id, E.e_name, C.c_name, O.o_name, E.e_datetime, E.e_location
    FROM EVENT E
    JOIN CATEGORY C ON E.c_id = C.c_id
    JOIN ORGANIZER O ON E.o_id = O.o_id
    ORDER BY E.e_datetime;
    """
    result = db.execute_query(query)
    return result if result else []

def search_events(search_term):
    query = """
    SELECT E.e_id, E.e_name, C.c_name, O.o_name, E.e_datetime, E.e_location
    FROM EVENT E
    JOIN CATEGORY C ON E.c_id = C.c_id
    JOIN ORGANIZER O ON E.o_id = O.o_id
    WHERE E.e_name ILIKE %s OR O.o_name ILIKE %s
    ORDER BY E.e_datetime;
    """
    like_pattern = f"%{search_term}%"
    result = db.execute_query(query, (like_pattern, like_pattern))
    return result if result else []

def payment_processing(or_id, payment_method, amount):
    try:
        db.cursor.execute("BEGIN;")
        # 檢查訂單是否存在且為待付款狀態
        query = """
        SELECT payment_status FROM "ORDER" WHERE or_id = %s;
        """
        result = db.execute_query(query, (or_id,))
        if not result:
            db.cursor.execute("ROLLBACK;")
            return False, "Order does not exist."
        order = result[0]
        if order['payment_status'] != 'Pending':
            db.cursor.execute("ROLLBACK;")
            return False, "Order is not pending for payment."
        # 插入付款記錄
        query = """
        INSERT INTO PAYMENT (or_id, payment_method, payment_datetime, amount)
        VALUES (%s, %s, %s, %s) RETURNING p_id;
        """
        result = db.execute_query(query, (or_id, payment_method, datetime.now(), amount))
        if not result:
            db.cursor.execute("ROLLBACK;")
            return False, "Failed to record payment."
        # 更新訂單狀態
        query = """
        UPDATE "ORDER" SET payment_status = 'Paid' WHERE or_id = %s;
        """
        db.execute_query(query, (or_id,))
        db.cursor.execute("COMMIT;")
        return True, "Payment processed successfully."
    except Exception as e:
        db.cursor.execute("ROLLBACK;")
        print(f"Payment processing error: {e}")
        return False, "Failed to process payment."

def view_edit_user_info(cu_id, field, new_value):
    if field not in ['cu_name', 'pwd', 'email', 'phone_number', 'address']:
        return False, "Invalid field."
    try:
        query = sql.SQL("UPDATE CUSTOMER SET {field} = %s WHERE cu_id = %s;").format(
            field=sql.Identifier(field)
        )
        db.execute_query(query, (new_value, cu_id))
        return True, f"{field} updated successfully."
    except Exception as e:
        print(f"View/Edit user info error: {e}")
        return False, "Failed to update user info."

def list_history(cu_id):
    # This function can be similar to view_purchase_history
    return query_user_purchase_history(cu_id)

# 更多函數可根據需要添加
