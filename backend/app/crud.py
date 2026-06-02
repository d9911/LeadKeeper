"""
CRUD operations for LeadKeeper
"""
from sqlalchemy.orm import Session
from .models import Lead
from .schemas import LeadCreate
from .database import SessionLocal
import logging

logger = logging.getLogger(__name__)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass


def create_lead(lead_data: LeadCreate) -> Lead:
    """Create a new lead in the database"""
    # Validate that at least one contact method is provided
    if not lead_data.phone.strip() and not lead_data.email.strip():
        raise ValueError("At least one contact method (phone or email) is required")
    
    db = SessionLocal()
    try:
        db_lead = Lead(
            name=lead_data.name,
            phone=lead_data.phone if lead_data.phone else None,
            email=lead_data.email if lead_data.email else None,
            company=lead_data.company,
            comment=lead_data.comment,
            consent=lead_data.consent
        )
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)
        logger.info(f"Lead created: {db_lead.id} - {db_lead.name}")
        return db_lead
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating lead: {e}")
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