# models/tickets.py

from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from .database import Base

class Ticket(Base):
    __tablename__ = "TICKET"

    t_id = Column(Integer, primary_key=True, index=True)
    e_id = Column(Integer, ForeignKey("EVENT.e_id"), nullable=False)
    t_type = Column(String(10), nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)
    total_quantity = Column(Integer, nullable=False)
    remain_quantity = Column(Integer, nullable=False)

    # 關聯
    event = relationship("Event", back_populates="tickets")
    order_details = relationship("OrderDetail", back_populates="ticket")
