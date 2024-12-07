# models/category.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Category(Base):
    __tablename__ = "CATEGORY"

    c_id = Column(Integer, primary_key=True, index=True)
    c_name = Column(String(15), nullable=False, unique=True)

    # 關聯
    events = relationship("Event", back_populates="category")
