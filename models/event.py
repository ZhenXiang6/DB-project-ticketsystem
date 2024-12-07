# models/event.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Event(Base):
    __tablename__ = "EVENT"

    e_id = Column(Integer, primary_key=True, index=True)
    e_name = Column(String(15), nullable=False)
    c_id = Column(Integer, ForeignKey("CATEGORY.c_id"), nullable=False)
    o_id = Column(Integer, ForeignKey("ORGANIZER.o_id"), nullable=False)
    e_datetime = Column(DateTime, nullable=False)
    e_location = Column(String(15), nullable=False)  # Changed to VARCHAR(15) as per schema
    description = Column(Text, nullable=True)

    category = relationship("Category", back_populates="events")
    organizer = relationship("Organizer", back_populates="events")
    event_venues = relationship("EventVenue", back_populates="event", cascade="all, delete-orphan")
    venues = relationship(
        "Venue",
        secondary="EVENT_VENUE",
        back_populates="events",
        overlaps="event_venues"
    )
