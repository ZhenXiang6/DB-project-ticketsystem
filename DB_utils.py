# DB_utils.py

import sys
import psycopg2
from tabulate import tabulate
from threading import Lock
from models import Base, Customer, Category, Organizer, Event, Ticket, TicketType, Order, OrderDetail, Payment, Venue, EventVenue
from sqlalchemy.orm import sessionmaker
from models.database import engine

# 建立資料庫連接
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

def authenticate_user(username, password):
    # 簡單的身份驗證，實際應用中應使用加密
    try:
        user = session.query(Customer).filter_by(cu_name=username).first()
        if user and user.pwd == password:
            # 假設有一個字段表示用戶角色，這裡簡化處理
            # 例如，可以在 Customer 表中添加一個 role 字段
            role = 'User'  # 或 'Admin'，根據實際情況設定
            return user.cu_id, role
        else:
            return None, None
    except Exception as e:
        print(f"Authentication error: {e}")
        return None, None

def register_user(username, password, email):
    try:
        new_user = Customer(cu_name=username, pwd=password, email=email)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user.cu_id
    except Exception as e:
        session.rollback()
        print(f"Registration error: {e}")
        return None

def username_exists(username):
    return session.query(Customer).filter_by(cu_name=username).first() is not None

def userid_exist(userid):
    return session.query(Customer).filter_by(cu_id=userid).first() is not None

def list_available_events():
    try:
        events = session.query(Event).filter(Event.e_datetime >= func.now()).order_by(Event.e_datetime).all()
        if not events:
            return None
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
        return None

def get_event_details(event_id):
    try:
        event = session.query(Event).filter_by(e_id=event_id).first()
        if not event:
            return None
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
        return None

def list_ticket_types(event_id):
    try:
        ticket_types = session.query(TicketType).filter_by(e_id=event_id).all()
        if not ticket_types:
            return None
        data = []
        for tt in ticket_types:
            ticket = session.query(Ticket).filter_by(e_id=tt.e_id, t_type=tt.t_type).first()
            data.append([
                tt.t_type,
                tt.price,
                ticket.total_quantity,
                ticket.remain_quantity
            ])
        headers = ["Ticket Type", "Price", "Total Quantity", "Remaining Quantity"]
        return tabulate(data, headers=headers, tablefmt="github")
    except Exception as e:
        print(f"List ticket types error: {e}")
        return None

def buy_ticket(user_id, event_id, t_type, quantity):
    try:
        ticket = session.query(Ticket).filter_by(e_id=event_id, t_type=t_type).with_for_update().first()
        if not ticket:
            return False, "Invalid ticket type selected."
        if ticket.remain_quantity < quantity:
            return False, f"Only {ticket.remain_quantity} tickets remaining."

        total_amount = ticket.price * quantity

        # 創建訂單
        new_order = Order(cu_id=user_id, or_date=datetime.now(), total_amount=total_amount, payment_status='Pending')
        session.add(new_order)
        session.commit()
        session.refresh(new_order)

        # 創建訂單明細
        order_detail = OrderDetail(or_id=new_order.or_id, t_id=ticket.t_id, quantity=quantity, subtotal=total_amount)
        session.add(order_detail)

        # 更新票數
        ticket.remain_quantity -= quantity

        session.commit()
        return True, f"Successfully purchased {quantity} ticket(s) for Event ID {event_id}."
    except Exception as e:
        session.rollback()
        print(f"Buy ticket error: {e}")
        return False, f"Purchase failed: {str(e)}"

def list_user_purchases_history(user_id):
    try:
        orders = session.query(Order).filter_by(cu_id=user_id).order_by(Order.or_date.desc()).all()
        if not orders:
            return None
        data = []
        for order in orders:
            for detail in order.order_details:
                data.append([
                    order.or_id,
                    detail.ticket.event.e_name,
                    detail.ticket.t_type,
                    detail.quantity,
                    detail.unit_price,
                    order.or_date.strftime('%Y-%m-%d %H:%M:%S'),
                    order.payment_status
                ])
        headers = ["Order ID", "Event Name", "Ticket Type", "Quantity", "Unit Price", "Order Date", "Payment Status"]
        return tabulate(data, headers=headers, tablefmt="github")
    except Exception as e:
        print(f"List user purchases history error: {e}")
        return None

def list_pending_orders(user_id):
    try:
        orders = session.query(Order).filter_by(cu_id=user_id, payment_status='Pending', is_canceled=False).all()
        if not orders:
            return None
        data = []
        for order in orders:
            data.append([
                order.or_id,
                order.or_date.strftime('%Y-%m-%d %H:%M:%S'),
                order.total_amount,
                order.payment_status
            ])
        headers = ["Order ID", "Order Date", "Total Amount", "Payment Status"]
        return tabulate(data, headers=headers, tablefmt="github")
    except Exception as e:
        print(f"List pending orders error: {e}")
        return None

def process_payment(user_id, or_id, payment_method):
    try:
        order = session.query(Order).filter_by(or_id=or_id, cu_id=user_id, payment_status='Pending', is_canceled=False).first()
        if not order:
            return False, "No pending order found with the provided Order ID."

        # 創建付款記錄
        payment = Payment(or_id=or_id, payment_method=payment_method, payment_datetime=datetime.now(), amount=order.total_amount)
        session.add(payment)

        # 更新訂單狀態
        order.payment_status = 'Paid'

        session.commit()
        return True, f"Payment of {order.total_amount} for Order ID {or_id} has been successfully processed."
    except Exception as e:
        session.rollback()
        print(f"Process payment error: {e}")
        return False, f"Payment failed: {str(e)}"

def view_edit_user_info(user_id, field, new_value):
    try:
        user = session.query(Customer).filter_by(cu_id=user_id).first()
        if not user:
            return False, "User not found."
        setattr(user, field, new_value)
        session.commit()
        return True, f"{field.replace('_', ' ').title()} has been updated successfully."
    except Exception as e:
        session.rollback()
        print(f"View/Edit user info error: {e}")
        return False, f"Update failed: {str(e)}"

def list_user_purchases(user_id):
    try:
        orders = session.query(Order).filter_by(cu_id=user_id, is_canceled=False).all()
        if not orders:
            return None
        data = []
        for order in orders:
            for detail in order.order_details:
                data.append([
                    order.or_id,
                    detail.ticket.event.e_name,
                    detail.ticket.t_type,
                    detail.quantity,
                    detail.unit_price,
                    detail.subtotal,
                    order.or_date.strftime('%Y-%m-%d %H:%M:%S'),
                    order.payment_status
                ])
        headers = ["Order ID", "Event Name", "Ticket Type", "Quantity", "Unit Price", "Subtotal", "Order Date", "Payment Status"]
        return tabulate(data, headers=headers, tablefmt="github")
    except Exception as e:
        print(f"List user purchases error: {e}")
        return None

def list_categories():
    try:
        categories = session.query(Category).order_by(Category.c_id).all()
        if not categories:
            return None
        data = []
        for c in categories:
            data.append([c.c_id, c.c_name])
        headers = ["Category ID", "Category Name"]
        return tabulate(data, headers=headers, tablefmt="github")
    except Exception as e:
        print(f"List categories error: {e}")
        return None

def list_organizers():
    try:
        organizers = session.query(Organizer).order_by(Organizer.o_id).all()
        if not organizers:
            return None
        data = []
        for o in organizers:
            data.append([o.o_id, o.o_name, o.contact_info])
        headers = ["Organizer ID", "Organizer Name", "Contact Info"]
        return tabulate(data, headers=headers, tablefmt="github")
    except Exception as e:
        print(f"List organizers error: {e}")
        return None

def add_event(e_name, c_id, o_id, e_datetime, e_location, description):
    try:
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
        return True, f"Event '{e_name}' added successfully with Event ID {event.e_id}."
    except Exception as e:
        session.rollback()
        print(f"Add event error: {e}")
        return False, f"Failed to add event: {str(e)}"

def issue_ticket(e_id, t_type, price, total_quantity):
    try:
        # 檢查活動是否存在
        event = session.query(Event).filter_by(e_id=e_id).first()
        if not event:
            return False, "Event ID does not exist."

        # 檢查票種是否已存在
        existing_tt = session.query(TicketType).filter_by(e_id=e_id, t_type=t_type).first()
        if existing_tt:
            return False, "Ticket type already exists for this event."

        # 創建 TicketType
        ticket_type = TicketType(e_id=e_id, t_type=t_type, price=price)
        session.add(ticket_type)

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
    try:
        events = session.query(Event).join(Organizer).filter(
            (Event.e_name.ilike(f"%{search_term}%")) | 
            (Organizer.o_name.ilike(f"%{search_term}%"))
        ).all()
        if not events:
            return None
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
        return None
