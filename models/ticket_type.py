# models/ticket_type.py

from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class TicketType(Base):
    __tablename__ = "TICKET_TYPE"

    e_id = Column(Integer, ForeignKey("EVENT.e_id"), primary_key=True, nullable=False)
    t_type = Column(String(10), primary_key=True, nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)

    # 關聯
    event = relationship("Event", back_populates="ticket_types")
    tickets = relationship("Ticket", back_populates="ticket_type")

