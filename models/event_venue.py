# models/event_venue.py

from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class EventVenue(Base):
    __tablename__ = "EVENT_VENUE"

    e_id = Column(Integer, ForeignKey("EVENT.e_id"), primary_key=True, nullable=False)
    v_id = Column(Integer, ForeignKey("VENUE.v_id"), primary_key=True, nullable=False)
    arrangement = Column(Text, nullable=True)

    # 關聯
    event = relationship("Event", back_populates="event_venues")
    venue = relationship("Venue", back_populates="event_venues")
