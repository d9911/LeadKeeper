"""
LeadKeeper - Lead Capture Module
FastAPI backend for lead form submissions
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .models import Lead
from .schemas import LeadCreate, LeadResponse
from .crud import create_lead, get_leads
from .email_service import notify_owner, notify_user
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LeadKeeper API",
    description="Lead capture module API",
    version="1.0.0"
)

# CORS configuration for frontend
origins = [
    "http://localhost:5173",  # Vite default port
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "leadkeeper"}


@app.post("/api/leads", response_model=LeadResponse)
def create_lead_endpoint(lead: LeadCreate):
    """Create a new lead"""
    try:
        db_lead = create_lead(lead)
        
        # Prepare lead data for email notification
        lead_data = {
            'name': db_lead.name,
            'phone': db_lead.phone,
            'email': db_lead.email,
            'company': db_lead.company,
            'comment': db_lead.comment
        }
        created_at_str = db_lead.created_at.strftime('%d.%m.%Y %H:%M') if db_lead.created_at else datetime.now().strftime('%d.%m.%Y %H:%M')
        
        # Send notification to owner
        try:
            notify_owner(lead_data, created_at_str)
        except Exception as e:
            logger.warning(f"Failed to send owner notification: {e}")
        
        # Send confirmation to user if email provided
        if db_lead.email:
            try:
                notify_user(
                    email=db_lead.email,
                    name=db_lead.name,
                    comment=db_lead.comment or '',
                    created_at=created_at_str
                )
            except Exception as e:
                logger.warning(f"Failed to send user notification: {e}")
        
        return db_lead
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating lead: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/leads", response_model=list[LeadResponse])
def get_leads_endpoint():
    """Get all leads"""
    try:
        leads = get_leads()
        return leads
    except Exception as e:
        logger.error(f"Error getting leads: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/leads/count")
def get_leads_count():
    """Get count of leads"""
    try:
        from sqlalchemy.orm import Session
        count = get_leads().__len__()
        return {"count": count}
    except Exception as e:
        logger.error(f"Error getting leads count: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")