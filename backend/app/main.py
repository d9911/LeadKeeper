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
from sqlalchemy.orm import Session
from sqlalchemy import text
import os

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
        return db_lead
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/leads", response_model=list[LeadResponse])
def get_leads_endpoint():
    """Get all leads"""
    try:
        leads = get_leads()
        return leads
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/leads/count")
def get_leads_count():
    """Get count of leads"""
    try:
        db = Session(bind=engine)
        count = db.query(Lead).count()
        db.close()
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")