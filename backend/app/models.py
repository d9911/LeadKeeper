"""
SQLAlchemy models for LeadKeeper
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base


class Lead(Base):
    """Lead model - stores customer contact requests"""
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    comment = Column(Text, nullable=True)
    consent = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Lead(id={self.id}, name='{self.name}', phone='{self.phone}', email='{self.email}')>"

    @property
    def contact(self):
        """Legacy property for backwards compatibility"""
        return self.phone or self.email or ''