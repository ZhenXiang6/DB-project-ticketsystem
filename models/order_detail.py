# models/order_detail.py

from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from .database import Base

class OrderDetail(Base):
    __tablename__ = "ORDER_DETAIL"

    or_id = Column(Integer, ForeignKey("ORDER.or_id"), primary_key=True, nullable=False)
    t_id = Column(Integer, ForeignKey("TICKET.t_id"), primary_key=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(DECIMAL(10,2), nullable=False)

    # 關聯
    order = relationship("Order", back_populates="order_details")
    ticket = relationship("Ticket", back_populates="order_details")
