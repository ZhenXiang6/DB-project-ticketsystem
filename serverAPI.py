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
    get_customer_detail_action
)
from utils import format_response, serialize_datetimes
from DB_utils import db

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
    success, message = signup_action(username, password, email)
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
    user = request.args.get('user')  # 假設有辦法從 request 中取得使用者
    if isinstance(user, Admin):
        e_name = data.get('e_name')
        c_id = data.get('c_id')
        o_id = data.get('o_id')
        e_datetime = data.get('e_datetime')
        e_location = data.get('e_location')
        description = data.get('description')
        event_id, message = user.add_event(e_name, c_id, o_id, e_datetime, e_location, description)
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
    user = request.args.get('user')  # 假設有辦法從 request 中取得使用者
    if isinstance(user, User):
        or_id = data.get('or_id')
        success, message = cancel_ticket_action(or_id, user.cu_id)
        if success:
            return send_json_response({"status": "success", "message": message})
        else:
            return send_json_response({"status": "error", "message": message}), 400
    else:
        return send_json_response({"status": "error", "message": "Please log in as a user."}), 403

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
    print(purchase_history)
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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8800)
