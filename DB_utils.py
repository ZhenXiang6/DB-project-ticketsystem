# DB_utils.py

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import sys
from datetime import datetime
from decimal import Decimal

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
    password='1234',  # 替換為您的密碼
    host='localhost',
    port=5432,
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

def register_user(username, password, email, address, phone):
    if username_exists(username):
        return None, "Username already exists."
    if email_exists(email):
        return None, "Email already exists."
    
    # 更新 INSERT 查詢，去掉 cu_id 讓資料庫自動處理
    query = """
    INSERT INTO CUSTOMER (cu_id, cu_name, pwd, email, address, phone_number) 
    VALUES (nextval('customer_cu_id_seq'), %s, %s, %s, %s, %s)
    RETURNING cu_id;
    """
    result = db.execute_query(query, (username, password, email, address, phone))
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

def add_event(e_name, c_name, o_name, e_datetime, e_location, description):
    # 使用 o_name 查找對應的 o_id
    print(o_name)
    query = """
    SELECT o_id FROM Organizer WHERE o_name = %s;
    """
    result = db.execute_query(query, (o_name,))
    
    if not result:
        return None, "Organizer not found."
    
    o_id = result[0]['o_id']  # 假設 Organizer 表格中有 o_id 和 o_name 欄位
    
    query = """
    SELECT c_id FROM category WHERE c_name = %s;
    """
    result = db.execute_query(query, (c_name,))
    
    if not result:
        return None, "Category not found."
    
    c_id = result[0]['c_id']  # 假設 Organizer 表格中有 o_id 和 o_name 欄位
    
    # 插入活動資料
    query = """
    INSERT INTO EVENT (e_id, e_name, c_id, o_id, e_datetime, e_location, description)
    VALUES (DEFAULT, %s, %s, %s, %s, %s, %s) RETURNING e_id;
    """
    result = db.execute_query(query, (e_name, c_id, o_id, e_datetime, e_location, description))
    
    if result:
        return result[0]['e_id'], "Event added successfully."
    return None, "Failed to add event."

def get_categories():
    query = """
    SELECT c_name FROM category;
    """
    result = db.execute_query(query)  # 假設 db.execute_query 是執行 SQL 查詢的函數

    if result:
        return result, ""  # 返回所有分類名稱
    else:
        return [], "No categories found."  # 如果查無資料，返回空列表和訊息



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

def query_user_purchase_history(cu_name):
    query = """
    SELECT O.or_id, E.e_name, T.t_type, OD.quantity, OD.subtotal, O.or_date, O.payment_status
    FROM "ORDER" O
    JOIN ORDER_DETAIL OD ON O.or_id = OD.or_id
    JOIN TICKET T ON OD.t_id = T.t_id
    JOIN EVENT E ON T.e_id = E.e_id
    JOIN CUSTOMER C ON C.cu_id = O.cu_id
    WHERE C.cu_name = %s
    ORDER BY O.or_date DESC;
    """
    result = db.execute_query(query, (cu_name,))
    return result if result else []

def buy_ticket(e_id, t_type, quantity, cu_id):
    try:
        db.cursor.execute("BEGIN;")
        # 檢查票券是否存在且有足夠的餘量，並鎖定該行
        query = "SELECT * FROM TICKET WHERE e_id = %s AND t_type = %s FOR UPDATE;"
        tickets = db.execute_query(query, (e_id, t_type))
        if not tickets:
            db.cursor.execute("ROLLBACK;")
            return False, "Ticket type does not exist for this event."
        ticket = tickets[0]
        if ticket['remain_quantity'] < quantity:
            db.cursor.execute("ROLLBACK;")
            return False, "Not enough tickets available."

        # 更新剩餘票券數量
        update_query = "UPDATE TICKET SET remain_quantity = remain_quantity - %s WHERE t_id = %s;"
        db.execute_query(update_query, (quantity, ticket['t_id']))

        # 創建訂單
        insert_order_query = """
        INSERT INTO "ORDER" (cu_id, or_date, total_amount, payment_status, is_canceled)
        VALUES (%s, %s, %s, %s, %s) RETURNING or_id;
        """
        total_amount = Decimal(ticket['price']) * quantity
        order = db.execute_query(insert_order_query, (cu_id, datetime.now(), total_amount, 'Pending', False))
        or_id = order[0]['or_id']

        # 創建訂單詳情
        insert_order_detail_query = """
        INSERT INTO ORDER_DETAIL (or_id, t_id, quantity, subtotal)
        VALUES (%s, %s, %s, %s);
        """
        db.execute_query(insert_order_detail_query, (or_id, ticket['t_id'], quantity, total_amount))

        db.cursor.execute("COMMIT;")
        return True, f"Successfully purchased {quantity} ticket(s) for event {e_id}."

    except Exception as e:
        db.cursor.execute("ROLLBACK;")
        print(f"Database error during ticket purchase: {e}")
        return False, "Failed to purchase ticket due to a server error."


def cancel_ticket(or_id, cu_name):
    try:
        db.cursor.execute("BEGIN;")
             
        # 檢查客戶是否存在
        query = "SELECT cu_id FROM customer WHERE cu_name = %s;"
        result = db.execute_query(query, (cu_name,))
        if not result:
            db.cursor.execute("ROLLBACK;")
            return False, "Customer does not exist."
        cu_id = result[0]['cu_id']
        
        # 檢查訂單是否存在且可取消
        query = """
        SELECT payment_status, is_canceled 
        FROM "ORDER" 
        WHERE or_id = %s AND cu_id = %s;
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
        UPDATE "ORDER" 
        SET is_canceled = TRUE, payment_status = 'Canceled' 
        WHERE or_id = %s;
        """
        db.execute_query(query, (or_id,))

        # 恢復票券數量
        query = "SELECT t_id, quantity FROM ORDER_DETAIL WHERE or_id = %s;"
        details = db.execute_query(query, (or_id,))
        for detail in details:
            query = "UPDATE TICKET SET remain_quantity = remain_quantity + %s WHERE t_id = %s;"
            db.execute_query(query, (detail['quantity'], detail['t_id']))

        # 提交事務
        db.cursor.execute("COMMIT;")
        return True, "Order canceled successfully."
    except Exception as e:
        db.cursor.execute("ROLLBACK;")
        print(f"Cancel ticket error: {e}")
        return False, "Failed to cancel order."

def view_event_details(e_id):
    query = """
    SELECT T.t_type, T.price, T.total_quantity, T.remain_quantity
    FROM EVENT E
    JOIN CATEGORY C ON E.c_id = C.c_id
    JOIN ORGANIZER O ON E.o_id = O.o_id
    JOIN TICKET T ON T.e_id = E.e_id
    WHERE E.e_id = %s;
    """
    result = db.execute_query(query, (e_id,))
    if result:
        return result
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

def customer_detail(cu_name):
    query = """
    SELECT cu_name, email, phone_number, address, role
    FROM CUSTOMER
    WHERE cu_name = %s;
    """
    # 假設 db.execute_query 支援參數化查詢
    result = db.execute_query(query, (cu_name,))

    # 返回查詢結果
    return result

def get_admin_organization(cu_name):
    if not cu_name:  # Check if username is provided
        return False, {"error": "Username is required"}  # Return False and error message
    
    try:
        # Step 1: Check if the user is an admin
        role_query = """
        SELECT C.role
        FROM CUSTOMER AS C
        WHERE C.cu_name = %s;
        """
        result = db.execute_query(role_query, (cu_name,))
        
        # Check if the user exists
        if not result:
            return False, {"error": "User not found"}  # User not found
        
        # Check if the user is an admin
        if result[0]['role'] != 'Admin':
            return False, {"error": "User is not an admin"}  # User is not an admin

        # Step 2: If the user is an admin, fetch the organizer info
        organizer_query = """
        SELECT o_id, o_name
        FROM organizer AS O
        JOIN Admin_Organize AS AO ON AO.organize_id = O.o_id
        WHERE AO.username = %s;
        """
        organizer_result = db.execute_query(organizer_query, (cu_name,))
        
        # Check if any organizers are found
        if not organizer_result:
            return False, {"error": "No organizers found for this admin"}  # No organizers found

        # Return success and the organizer result
        return True, organizer_result
    except Exception as e:
        # Return general error on failure
        return False, {"error": f"An error occurred: {str(e)}"}  # Internal Server Error

def list_categories():
    query = "SELECT c_id, c_name FROM CATEGORY ORDER BY c_id;"
    result = db.execute_query(query)
    return result if result else []

def list_event_by_category(c_id):
    query = """
    SELECT E.e_id, E.e_name, C.c_name, O.o_name, E.e_datetime, E.e_location
    FROM EVENT E
    JOIN CATEGORY C ON E.c_id = C.c_id
    JOIN ORGANIZER O ON E.o_id = O.o_id
    WHERE E.c_id = %s
    ORDER BY E.e_datetime;
    """
    result = db.execute_query(query, (c_id,))
    return result if result else []


def reset_all_sequences():
    # 定義表名、序列名稱與對應的 ID 欄位
    tables_sequences = {
        'category': ('category_c_id_seq', 'c_id'),
        'organizer': ('organizer_o_id_seq', 'o_id'),
        'event': ('event_e_id_seq', 'e_id'),
        'ticket': ('ticket_t_id_seq', 't_id'),
        'customer': ('customer_cu_id_seq', 'cu_id'),
        'ORDER': ('"ORDER_or_id_seq"', 'or_id'),
        'payment': ('payment_p_id_seq', 'p_id'),
        'venue': ('venue_v_id_seq', 'v_id')
    }

    for table, (sequence, id_col) in tables_sequences.items():
            # 使用 Literal 來傳遞序列名稱作為字串
            query = sql.SQL("""
                SELECT setval(
                    {sequence},
                    COALESCE((SELECT MAX({id_col}) FROM {table}), 0) + 1,
                    false
                );
            """).format(
                sequence=sql.Literal(sequence),
                table=sql.Identifier(table),
                id_col=sql.Identifier(id_col)
            )
            db.execute_query(query)

def get_sales_report(e_id):
    """
    根據 event_id 生成銷售報告，包含每個票種的售出數量及收入，和總收入。

    :param e_id: 活動的唯一識別碼
    :return: 銷售報告數據字典或空字典
    """
    try:
        query = """
        SELECT 
            T.t_type,
            SUM(OD.quantity) AS tickets_sold,
            SUM(OD.subtotal) AS revenue
        FROM TICKET T
        JOIN ORDER_DETAIL OD ON T.t_id = OD.t_id
        JOIN "ORDER" O ON OD.or_id = O.or_id
        WHERE T.e_id = %s AND O.payment_status = 'Paid'
        GROUP BY T.t_type;
        """
        report_data = db.execute_query(query, (e_id,))
        if report_data:
            # 計算總收入
            total_revenue = sum(item['revenue'] for item in report_data)
            return {
                "event_id": e_id,
                "ticket_details": report_data,
                "total_revenue": total_revenue
            }
        else:
            return {}
    except Exception as e:
        print(f"Error generating sales report: {e}")
        return {}