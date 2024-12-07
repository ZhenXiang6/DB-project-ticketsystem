# models/payment.py

from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, TIMESTAMP, String
from sqlalchemy.orm import relationship
from .database import Base

class Payment(Base):
    __tablename__ = "PAYMENT"

    p_id = Column(Integer, primary_key=True, index=True)
    or_id = Column(Integer, ForeignKey("ORDER.or_id"), nullable=False)
    payment_method = Column(String(10), nullable=False)
    payment_datetime = Column(TIMESTAMP, nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)

    # 關聯
    order = relationship("Order", back_populates="payment")
