# models/users.py

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from .database import Base

class Customer(Base):
    __tablename__ = "CUSTOMER"

    cu_id = Column(Integer, primary_key=True, index=True)
    cu_name = Column(String(15), nullable=False)
    email = Column(String(15), unique=True, nullable=False)
    phone_number = Column(String(15), nullable=True)
    address = Column(Text, nullable=True)

    # 關聯
    orders = relationship("Order", back_populates="customer")
