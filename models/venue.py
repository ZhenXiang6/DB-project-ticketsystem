# models/venue.py

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from .database import Base

class Venue(Base):
    __tablename__ = "VENUE"

    v_id = Column(Integer, primary_key=True, index=True)
    v_name = Column(String(15), nullable=False, unique=True)
    address = Column(Text, nullable=True)
    capacity = Column(Integer, nullable=False)
    contact_info = Column(String(15), nullable=True)

    # 關聯
    seats = relationship("Seat", back_populates="venue")
    event_venues = relationship("EventVenue", back_populates="venue")
    events = relationship("Event", secondary="EVENT_VENUE", back_populates="venues")
