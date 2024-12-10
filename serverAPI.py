from flask import Flask, request, jsonify, session
from datetime import datetime
from decimal import Decimal
from role import Admin, User
from flask_cors import CORS
import json
from action import (
    signup_action,
    login_action,
    exit_action,
    add_event_action,
    issue_tickets_action,
    query_user_info_action,
    query_user_purchase_history_action,
    buy_ticket_action,
    cancel_ticket_action,
    view_event_details_action,
    list_event_action,
    search_event_action,
    payment_action,
    view_edit_user_info_action,
    view_purchase_history_action,
    list_history_action,
    get_customer_detail_action,
    get_admin_organize_action,
    get_categories_action,
)
from utils import format_response, serialize_datetimes
from DB_utils import db, reset_all_sequences, get_sales_report

app = Flask(__name__)

CORS(app, origins=["http://localhost:5173"])

online_users = {}

# 用於 JSON 序列化的 DateTime 和 Decimal 編碼器
class DateTimeDecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return str(obj)  # 使用 str 保持精度
        return super().default(obj)

# 預設的 response formatter
def send_json_response(response):
    return jsonify(response)

# 註冊 API 路由
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    address = data.get('address')
    phone = data.get('phone')
    success, message = signup_action(username, password, email, address, phone)
    if success:
        return send_json_response({"status": "success", "message": message})
    else:
        return send_json_response({"status": "error", "message": message}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    success, result = login_action(username, password)
    if success:
        cu_id = result['cu_id']
        role = result['role']
        user = Admin(cu_id, role) if role.lower() == 'admin' else User(cu_id, role)
        online_users[username] = user
        return send_json_response({"status": "success", "message": f"Logged in as {role}.", "role": role})
    else:
        return send_json_response({"status": "error", "message": result}), 400

@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()  # Retrieve JSON data from the body of the request
    cu_name = data.get('cu_name')

    if cu_name:
        if cu_name in online_users:
            online_users.pop(cu_name, None)  # Remove user from the online_users dictionary
        return send_json_response({"status": "success", "message": "Logged out successfully."})
    else:
        return send_json_response({"status": "error", "message": "You are not logged in."}), 400



@app.route('/addevent', methods=['POST'])
def add_event():
    data = request.get_json()
    role = request.args.get('role')  # 假設有辦法從 request 中取得使用者
    if role == "Admin":
        e_name = data.get('e_name')
        c_name = data.get('c_name')
        o_name = data.get('o_name')
        e_datetime = data.get('e_datetime')
        e_location = data.get('e_location')
        description = data.get('description')
        event_id, message = add_event_action(e_name, c_name, o_name, e_datetime, e_location, description)
        if event_id:
            return send_json_response({"status": "success", "message": message, "e_id": event_id})
        else:
            return send_json_response({"status": "error", "message": message}), 400
    else:
        return send_json_response({"status": "error", "message": "Unauthorized action. Admins only."}), 403

@app.route('/buyticket', methods=['POST'])
def buy_ticket():
    data = request.get_json()
    user_name = request.args.get('user_name')  # 假設有辦法從 request 中取得使用者
    
    user = None
    if user_name in online_users:
        user = online_users[user_name]
    
    if isinstance(user, User):
        e_id = data.get('e_id')
        t_type = data.get('t_type')
        quantity = data.get('quantity')
        cu_id = user.cu_id
        success, message = buy_ticket_action(e_id, t_type, quantity, cu_id)
        if success:
            return send_json_response({"status": "success", "message": message}), 200
        else:
            return send_json_response({"status": "error", "message": message}), 400
    else:
        return send_json_response({"status": "error", "message": "Please log in as a user."}), 403

@app.route('/cancelticket', methods=['POST'])
def cancel_ticket():
    data = request.get_json()
    user_name = request.args.get('user_name')
    
    if not data:
        return jsonify({"status": "error", "message": "Invalid request. No data provided."}), 400
    
    or_id = data.get('or_id')

    user = online_users.get(user_name)

    if not isinstance(user, User):
        return jsonify({"status": "error", "message": "Please log in as a user."}), 401

    
    success, message = cancel_ticket_action(or_id, user_name)

    if success:
        response = {"status": "success", "message": message}
        return jsonify(response), 200
    else:
        response = {"status": "error", "message": message}
        return jsonify(response), 400

@app.route('/view_event_details', methods=['GET'])
def view_event_details():
    e_id = request.args.get('e_id')
    
    details = view_event_details_action(e_id)
    
    if details:
        details = serialize_datetimes(details)
        return send_json_response({"status": "success", "data": details})
    else:
        return send_json_response({"status": "error", "message": "Event not found."}), 404

# 設置其他路由，按照相似邏輯處理不同功能...

@app.route('/get_all_event_detail', methods=['GET'])
def get_all_event_detail():
    details = list_event_action()
    
    if details:
        return send_json_response({"status": "success", "data": details})
    else:
        return send_json_response({"status": "error", "message": "Event not found."}), 404

   
@app.route('/exit', methods=['POST'])
def exit_system():
    message = exit_action()
    return send_json_response({"status": "success", "message": message})

@app.route('/customer_detail', methods=['GET'])
def get_customer_detail():
    cu_name = request.args.get('cu_name')  # 从请求中取得 cu_name
    
    if not cu_name:
        return jsonify({"error": "Missing customer name"}), 400  # 若缺少 cu_name，返回错误
    
    user_detail = get_customer_detail_action(cu_name)
    
    # 如果找不到資料，給出未填寫的訊息
    if user_detail is None or user_detail == []:
        return jsonify({"message": "未填寫"}), 200  # 返回未填寫訊息
    
    # 對於每一個屬性進行處理，若為 None 則顯示 "未填寫"
    if isinstance(user_detail, dict):
        for key, value in user_detail.items():
            if value is None:
                user_detail[key] = "未填寫"
    
    # 返回填寫的或處理過的資料
    return jsonify(user_detail), 200

@app.route('/user_purchase_history', methods=['GET'])
def get_user_purchase_history():
    # Get the 'cu_name' parameter from the query string
    cu_name = request.args.get('cu_name')
    
    # Handle missing 'cu_name' gracefully
    if not cu_name:
        return jsonify({"error": "Missing 'cu_name' parameter"}), 400
    
    # Query the purchase history
    purchase_history = query_user_purchase_history_action(cu_name)
    
    # Return the response
    if purchase_history:
        return jsonify({"cu_name": cu_name, "purchase_history": purchase_history}), 200
    else:
        return jsonify({"cu_name": cu_name, "message": "No purchase history found"}), 404

@app.route('/payment', methods=['POST'])
def payment():
    user_name = request.args.get('user_name')  
    user = online_users.get(user_name)  
    
    if user and isinstance(user, User):  
        data = request.get_json()
        or_id = data.get('or_id')
        payment_method = data.get('payment_method')
        amount = data.get('amount')

        if not all([or_id, payment_method, amount]):
            return jsonify({"status": "error", "message": "Missing required fields."}), 400

        success, message = payment_action(or_id, payment_method, amount)
        
        if success:
            response = {"status": "success", "message": message}
        else:
            response = {"status": "error", "message": message}
    else:
        response = {"status": "error", "message": "Please log in as a user."}

    return jsonify(response)

# In serverAPI.py
@app.route('/get_admin_organize', methods=['GET'])
def get_admin_organize():
    username = request.args.get('cu_name')  # Get the username from the request
    
    if not username:  # Step 1: Validate username
        response = {"status": "error", "message": "Username is required"}
        return jsonify(response), 400

    # Step 2: Get the admin's organization data
    success, result = get_admin_organize_action(username)

    if not success:  # If failure occurred, return the error
        response = {"status": "error", "message": result["error"]}
        return jsonify(response), 400  # Use 400 for errors like invalid admin
    
    # Step 3: Return the successful result
    response = {
        "status": "success",
        "o_id": result[0]["o_id"],
        "o_name": result[0]["o_name"]
    }
    return jsonify(response)

@app.route('/issue_tickets', methods=['POST'])
def issue_tickets():
    params = request.json
    e_id = params.get('e_id')
    t_type = params.get('t_type')
    price = params.get('price')
    total_quantity = params.get('total_quantity')

    success, message = issue_tickets_action(e_id, t_type, price, total_quantity)

    if success:
        return jsonify({"status": "success", "message": message}), 200
    else:
        return jsonify({"status": "error", "message": message}), 400
    
@app.route('/get_categories', methods=['GET'])
def get_categories():
    result = get_categories_action()  # 假設 db.execute_query 是執行 SQL 查詢的函數

    if result:
        return jsonify({"status": "success", "categories": result}), 200
    else:
        return jsonify({"status": "error", "message": "No categories found."}), 404

@app.route('/generate_sales_report', methods=['POST'])
def generate_sales_report():
    try:
        # 獲取請求參數
        params = request.json
        if not params:
            return jsonify({"status": "error", "message": "Missing request body."}), 400

        event_id = params.get('event_id')
        if event_id is None:
            return jsonify({"status": "error", "message": "Missing event_id parameter."}), 400

        # 獲取銷售報告
        report = get_sales_report(event_id)
        if report:
            return jsonify({"status": "success", "data": report}), 200
        else:
            return jsonify({"status": "error", "message": "No sales data found for the given event_id."}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/reset_all_sequences', methods=['POST'])
def reset_sequences():
    try:
        result = reset_all_sequences()
        if result["status"] == "success":
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8800)
