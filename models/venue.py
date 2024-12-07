# models/venue.py

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from .database import Base

class Venue(Base):
    __tablename__ = "VENUE"

    v_id = Column(Integer, primary_key=True, index=True)
    v_name = Column(String(15), nullable=False)
    address = Column(Text, nullable=True)
    capacity = Column(Integer, nullable=False)
    contact_info = Column(String(15), nullable=True)

    event_venues = relationship("EventVenue", back_populates="venue", cascade="all, delete-orphan")
    events = relationship(
        "Event",
        secondary="EVENT_VENUE",
        back_populates="venues",
        overlaps="event_venues"
    )
