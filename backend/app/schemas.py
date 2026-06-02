"""
Pydantic schemas for LeadKeeper API
"""
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional


class LeadCreate(BaseModel):
    """Schema for creating a new lead"""
    name: str
    contact: str
    company: Optional[str] = None
    comment: Optional[str] = None
    consent: bool

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

    @field_validator('contact')
    @classmethod
    def contact_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Contact cannot be empty')
        return v.strip()

    @field_validator('consent')
    @classmethod
    def consent_must_be_true(cls, v: bool) -> bool:
        if not v:
            raise ValueError('Consent must be provided')
        return v


class LeadResponse(BaseModel):
    """Schema for lead response"""
    id: int
    name: str
    contact: str
    company: Optional[str] = None
    comment: Optional[str] = None
    consent: bool
    created_at: datetime

    class Config:
        from_attributes = True