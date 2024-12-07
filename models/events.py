# models/events.py

from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base

class Event(Base):
    __tablename__ = "EVENT"

    e_id = Column(Integer, primary_key=True, index=True)
    e_name = Column(String(15), nullable=False)
    c_id = Column(Integer, ForeignKey("CATEGORY.c_id"), nullable=False)
    o_id = Column(Integer, ForeignKey("ORGANIZER.o_id"), nullable=False)
    e_datetime = Column(TIMESTAMP, nullable=False)
    e_location = Column(String(15), nullable=False)
    description = Column(Text, nullable=True)

    # 關聯
    category = relationship("Category", back_populates="events")
    organizer = relationship("Organizer", back_populates="events")
    tickets = relationship("Ticket", back_populates="event")
    event_venues = relationship("EventVenue", back_populates="event")
    venues = relationship("Venue", secondary="EVENT_VENUE", back_populates="events")
