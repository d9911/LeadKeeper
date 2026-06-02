"""
CRUD operations for LeadKeeper
"""
from sqlalchemy.orm import Session
from .models import Lead
from .schemas import LeadCreate
from .database import SessionLocal
import re


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass


def validate_contact(contact: str) -> bool:
    """
    Validate contact field - should be email or phone
    Basic validation: contains @ for email or digits for phone
    """
    if not contact:
        return False
    
    # Check if it looks like email
    if '@' in contact and '.' in contact:
        return True
    
    # Check if it contains digits (phone)
    if any(c.isdigit() for c in contact):
        return True
    
    return False


def create_lead(lead_data: LeadCreate) -> Lead:
    """Create a new lead in the database"""
    # Validate contact format
    if not validate_contact(lead_data.contact):
        raise ValueError("Contact should be a valid email or phone number")
    
    db = SessionLocal()
    try:
        db_lead = Lead(
            name=lead_data.name,
            contact=lead_data.contact,
            company=lead_data.company,
            comment=lead_data.comment,
            consent=lead_data.consent
        )
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)
        return db_lead
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_leads() -> list[Lead]:
    """Get all leads from the database, ordered by creation date (newest first)"""
    db = SessionLocal()
    try:
        leads = db.query(Lead).order_by(Lead.created_at.desc()).all()
        return leads
    finally:
        db.close()