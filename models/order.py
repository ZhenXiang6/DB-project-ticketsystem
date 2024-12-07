# models/order.py

from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, TIMESTAMP, String, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class Order(Base):
    __tablename__ = "ORDER"

    or_id = Column(Integer, primary_key=True, index=True)
    cu_id = Column(Integer, ForeignKey("CUSTOMER.cu_id"), nullable=False)
    or_date = Column(TIMESTAMP, nullable=False)
    total_amount = Column(DECIMAL(10,2), nullable=False)
    payment_status = Column(String(10), nullable=False, default='Pending')
    is_canceled = Column(Boolean, nullable=False, default=False)

    # 關聯
    customer = relationship("Customer", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)
