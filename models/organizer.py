# models/organizer.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Organizer(Base):
    __tablename__ = "ORGANIZER"

    o_id = Column(Integer, primary_key=True, index=True)
    o_name = Column(String(15), nullable=False, unique=True)
    contact_info = Column(String(15), nullable=True)

    # 關聯
    events = relationship("Event", back_populates="organizer")
