# models/user.py

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from .database import Base

class Customer(Base):
    __tablename__ = "CUSTOMER"

    cu_id = Column(Integer, primary_key=True, index=True)
    cu_name = Column(String(15), nullable=False, unique=True)
    email = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(15), nullable=True)
    address = Column(Text, nullable=True)
    pwd = Column(String(128), nullable=False)  # 明文密碼
    role = Column(String(10), nullable=False, default='User')  # 'User' 或 'Admin'

    # Relationships
    orders = relationship("Order", back_populates="customer")
