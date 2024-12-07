# DB_utils.py

import sys
import psycopg2
from tabulate import tabulate
from threading import Lock
from models import (
    Base, Customer, Category, Organizer, Event, Ticket,
    Order, OrderDetail, Payment, Venue, EventVenue
)
from sqlalchemy.orm import sessionmaker
from models.database import engine
from sqlalchemy import func
from datetime import datetime

# 建立資料庫連接
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

def authenticate_user(username, password):
    """
    驗證用戶名和密碼，返回用戶 ID 和角色
    """
    try:
        user = session.query(Customer).filter_by(cu_name=username).first()
        if user and user.check_password(password):
            return user.cu_id, user.role
        else:
            return None, None
    except Exception as e:
        print(f"Authentication error: {e}")
        return None, None

def register_user(username, password, email):
    """
    註冊新用戶，返回用戶 ID
    """
    try:
        if username_exists(username):
            print("Username already exists.")
            return None
        new_user = Customer(cu_name=username, email=email)
        new_user.set_password(password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user.cu_id
    except Exception as e:
        session.rollback()
        print(f"Registration error: {e}")
        return None

def username_exists(username):
    """
    檢查用戶名是否已存在
    """
    return session.query(Customer).filter_by(cu_name=username).first() is not None

def userid_exist(userid):
    """
    檢查用戶 ID 是否存在
    """
    return session.query(Customer).filter_by(cu_id=userid).first() is not None

def list_available_events():
    """
    列出所有即將舉行的活動
    """
    try:
        events = session.query(Event).filter(Event.e_datetime >= func.now()).order_by(Event.e_datetime).all()
        if not events:
            return "No available events."
        data = []
        for event in events:
            data.append([
                event.e_id,
                event.e_name,
                event.category.c_name,
                event.organizer.o_name,
                event.e_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                event.e_location
            ])
        headers = ["Event ID", "Event Name", "Category", "Organizer", "Date & Time", "Location"]
        return tabulate(data, headers=headers, tablefmt="github")
    except Exception as e:
        print(f"List available events error: {e}")
        return "Error listing available events."

def get_event_details(event_id):
    """
    獲取特定活動的詳細資訊
    """
    try:
        event = session.query(Event).filter_by(e_id=event_id).first()
        if not event:
            return "Event not found."
        data = [[
            event.e_id,
            event.e_name,
            event.category.c_name,
            event.organizer.o_name,
            event.e_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            event.e_location,
            event.description
        ]]
        headers = ["Event ID", "Event Name", "Category", "Organizer", "Date & Time", "Location", "Description"]
        return tabulate(data, headers=headers, tablefmt="github")
    except Exception as e:
        print(f"Get event details error: {e}")
        return "Error retrieving event details."

def list_ticket_types(event_id):
    """
    列出指定活動的所有票種
    """
    try:
        tickets = session.query(Ticket).filter_by(e_id=event_id).all()
        if not tickets:
            return "No ticket types available for this event."
        data = []
        for ticket in tickets:
            data.append([
                ticket.t_type,
                f"{ticket.price:.2f}",
                ticket.total_quantity,
                ticket.remain_quantity
            ])
        headers = ["Ticket Type", "Price", "Total Quantity", "Remaining Quantity"]
        return tabulate(data, headers=headers, tablefmt="github")
    except Exception as e:
        print(f"List ticket types error: {e}")
        return "Error listing ticket types."

def purchase_ticket(user_id, event_id, ticket_type, quantity):
    """
    購買票券，返回成功與否以及訊息
    """
    try:
        # 鎖定票券行以避免並發問題
        ticket = session.query(Ticket).filter_by(e_id=event_id, t_type=ticket_type).with_for_update().first()
        if not ticket:
            return False, "Invalid ticket type or event ID."
        if ticket.remain_quantity < quantity:
            return False, f"Only {ticket.remain_quantity} tickets available."

        # 計算總金額
        total_amount = float(ticket.price) * quantity

        # 創建訂單
        new_order = Order(
            cu_id=user_id,
            or_date=datetime.now(),
            total_amount=total_amount,
            payment_status='Pending',
            is_canceled=False
        )
        session.add(new_order)
        session.commit()
        session.refresh(new_order)

        # 創建訂單明細
        order_detail = OrderDetail(
            or_id=new_order.or_id,
            t_id=ticket.t_id,
            quantity=quantity,
            subtotal=total_amount
        )
        session.add(order_detail)

        # 更新票券剩餘數量
        ticket.remain_quantity -= quantity

        session.commit()
        return True, f"Successfully purchased {quantity} ticket(s) for Event ID {event_id}."
    except Exception as e:
        session.rollback()
        print(f"Purchase ticket error: {e}")
        return False, f"Purchase failed: {str(e)}"

def list_user_purchases_history(user_id):
    """
    列出用戶的購票歷史
    """
    try:
        orders = session.query(Order).filter_by(cu_id=user_id).order_by(Order.or_date.desc()).all()
        if not orders:
            return "No purchase history found."
        data = []
        for order in orders:
            for detail in order.order_details:
                data.append([
                    order.or_id,
                    detail.ticket.event.e_name,
                    detail.ticket.t_type,
                    detail.quantity,
                    f"{detail.subtotal:.2f}",
                    order.or_date.strftime('%Y-%m-%d %H:%M:%S'),
                    order.payment_status
                ])
        headers = ["Order ID", "Event Name", "Ticket Type", "Quantity", "Subtotal", "Order Date", "Payment Status"]
        return tabulate(data, headers=headers, tablefmt="github")
    except Exception as e:
        print(f"List user purchases history error: {e}")
        return "Error listing purchase history."

def list_pending_orders(user_id):
    """
    列出用戶所有待付款的訂單
    """
    try:
        orders = session.query(Order).filter_by(cu_id=user_id, payment_status='Pending', is_canceled=False).all()
        if not orders:
            return "No pending orders found."
        data = []
        for order in orders:
            data.append([
                order.or_id,
                order.or_date.strftime('%Y-%m-%d %H:%M:%S'),
                f"{order.total_amount:.2f}",
                order.payment_status
            ])
        headers = ["Order ID", "Order Date", "Total Amount", "Payment Status"]
        return tabulate(data, headers=headers, tablefmt="github")
    except Exception as e:
        print(f"List pending orders error: {e}")
        return "Error listing pending orders."

def process_payment(user_id, or_id, payment_method):
    """
    處理付款，更新訂單狀態
    """
    try:
        order = session.query(Order).filter_by(or_id=or_id, cu_id=user_id, payment_status='Pending', is_canceled=False).first()
        if not order:
            return False, "No pending order found with the provided Order ID."

        # 創建付款記錄
        payment = Payment(
            or_id=or_id,
            payment_method=payment_method,
            payment_datetime=datetime.now(),
            amount=order.total_amount
        )
        session.add(payment)

        # 更新訂單狀態
        order.payment_status = 'Paid'

        session.commit()
        return True, f"Payment of {order.total_amount:.2f} for Order ID {or_id} has been successfully processed."
    except Exception as e:
        session.rollback()
        print(f"Process payment error: {e}")
        return False, f"Payment failed: {str(e)}"

def view_edit_user_info(user_id, field, new_value):
    """
    查看或編輯用戶資訊
    """
    try:
        user = session.query(Customer).filter_by(cu_id=user_id).first()
        if not user:
            return False, "User not found."
        if field not in ['cu_name', 'password', 'email', 'phone_number', 'address']:
            return False, "Invalid field selected."
        if field == 'password':
            user.set_password(new_value)
        else:
            setattr(user, field, new_value)
        session.commit()
        return True, f"{field.replace('_', ' ').title()} has been updated successfully."
    except Exception as e:
        session.rollback()
        print(f"View/Edit user info error: {e}")
        return False, f"Update failed: {str(e)}"

def list_user_purchases(user_id):
    """
    列出用戶所有購票紀錄
    """
    try:
        orders = session.query(Order).filter_by(cu_id=user_id, is_canceled=False).all()
        if not orders:
            return "No purchase records found."
        data = []
        for order in orders:
            for detail in order.order_details:
                data.append([
                    order.or_id,
                    detail.ticket.event.e_name,
                    detail.ticket.t_type,
                    detail.quantity,
                    f"{detail.subtotal:.2f}",
                    order.or_date.strftime('%Y-%m-%d %H:%M:%S'),
                    order.payment_status
                ])
        headers = ["Order ID", "Event Name", "Ticket Type", "Quantity", "Subtotal", "Order Date", "Payment Status"]
        return tabulate(data, headers=headers, tablefmt="github")
    except Exception as e:
        print(f"List user purchases error: {e}")
        return "Error listing user purchases."

def list_categories():
    """
    列出所有類別
    """
    try:
        categories = session.query(Category).order_by(Category.c_id).all()
        if not categories:
            return "No categories found."
        data = []
        for c in categories:
            data.append([c.c_id, c.c_name])
        headers = ["Category ID", "Category Name"]
        return tabulate(data, headers=headers, tablefmt="github")
    except Exception as e:
        print(f"List categories error: {e}")
        return "Error listing categories."

def list_organizers():
    """
    列出所有主辦方
    """
    try:
        organizers = session.query(Organizer).order_by(Organizer.o_id).all()
        if not organizers:
            return "No organizers found."
        data = []
        for o in organizers:
            data.append([o.o_id, o.o_name, o.contact_info])
        headers = ["Organizer ID", "Organizer Name", "Contact Info"]
        return tabulate(data, headers=headers, tablefmt="github")
    except Exception as e:
        print(f"List organizers error: {e}")
        return "Error listing organizers."

def add_event(e_name, c_id, o_id, e_datetime, e_location, description):
    """
    新增活動，返回成功與否及訊息
    """
    try:
        # 檢查類別是否存在
        category = session.query(Category).filter_by(c_id=c_id).first()
        if not category:
            return False, "Category ID does not exist."

        # 檢查主辦方是否存在
        organizer = session.query(Organizer).filter_by(o_id=o_id).first()
        if not organizer:
            return False, "Organizer ID does not exist."

        event = Event(
            e_name=e_name,
            c_id=c_id,
            o_id=o_id,
            e_datetime=e_datetime,
            e_location=e_location,
            description=description
        )
        session.add(event)
        session.commit()
        session.refresh(event)
        return True, f"Event '{e_name}' added successfully with Event ID {event.e_id}."
    except Exception as e:
        session.rollback()
        print(f"Add event error: {e}")
        return False, f"Failed to add event: {str(e)}"

def issue_ticket(e_id, t_type, price, total_quantity):
    """
    發行票券，返回成功與否及訊息
    """
    try:
        # 檢查活動是否存在
        event = session.query(Event).filter_by(e_id=e_id).first()
        if not event:
            return False, "Event ID does not exist."

        # 檢查票種是否已存在於 TICKET 表中
        existing_ticket = session.query(Ticket).filter_by(e_id=e_id, t_type=t_type).first()
        if existing_ticket:
            return False, "Ticket type already exists for this event."

        # 創建 Ticket
        ticket = Ticket(
            e_id=e_id,
            t_type=t_type,
            price=price,
            total_quantity=total_quantity,
            remain_quantity=total_quantity
        )
        session.add(ticket)
        session.commit()
        return True, f"Ticket type '{t_type}' issued successfully for Event ID {e_id}."
    except Exception as e:
        session.rollback()
        print(f"Issue ticket error: {e}")
        return False, f"Issue ticket failed: {str(e)}"

def search_events(search_term):
    """
    搜尋活動，根據活動名稱或主辦方名稱
    """
    try:
        events = session.query(Event).join(Organizer).filter(
            (Event.e_name.ilike(f"%{search_term}%")) | 
            (Organizer.o_name.ilike(f"%{search_term}%"))
        ).all()
        if not events:
            return "No events found matching the search criteria."
        data = []
        for event in events:
            data.append([
                event.e_id,
                event.e_name,
                event.category.c_name,
                event.organizer.o_name,
                event.e_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                event.e_location
            ])
        headers = ["Event ID", "Event Name", "Category", "Organizer", "Date & Time", "Location"]
        return tabulate(data, headers=headers, tablefmt="github")
    except Exception as e:
        print(f"Search events error: {e}")
        return "Error searching events."

def get_user_role(user_id):
    """
    查詢用戶的角色
    :param user_id: 用戶 ID
    :return: 用戶角色 ('User' 或 'Admin')
    """
    try:
        user = session.query(Customer).filter_by(cu_id=user_id).first()
        if user:
            return user.role  # 確保 role 欄位存在於 CUSTOMER 表
        return None
    except Exception as e:
        print(f"Error fetching user role: {e}")
        return None

def db_connect():
    """
    返回一個新的資料庫 Session 對象
    """
    try:
        SessionLocal = sessionmaker(bind=engine)
        new_session = SessionLocal()
        print("Database connection established successfully.")
        return new_session
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        raise

__all__ = [
    "authenticate_user",
    "register_user",
    "username_exists",
    "userid_exist",
    "list_available_events",
    "get_event_details",
    "list_ticket_types",
    "purchase_ticket",  # 確保這裡包含 purchase_ticket
    "list_user_purchases_history",
    "list_pending_orders",
    "process_payment",
    "view_edit_user_info",
    "list_user_purchases",
    "list_categories",
    "list_organizers",
    "add_event",
    "issue_ticket",
    "search_events",
    "get_user_role",
    "db_connect"
]
