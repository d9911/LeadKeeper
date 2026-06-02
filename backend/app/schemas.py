"""
Pydantic schemas for LeadKeeper API
"""
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
import re


class LeadCreate(BaseModel):
    """Schema for creating a new lead"""
    name: str
    phone: str = ""
    email: str = ""
    company: Optional[str] = None
    comment: Optional[str] = None
    consent: bool

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        if len(v.strip()) < 2:
            raise ValueError('Name is too short')
        if len(v.strip()) > 100:
            raise ValueError('Name is too long')
        return v.strip()

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not v or not v.strip():
            return ""
        
        # Remove formatting characters for validation
        clean_phone = v.replace(' ', '').replace('-', '').replace('.', '').replace('(', '').replace(')', '')
        
        # Check for multiple +
        if clean_phone.count('+') > 1:
            raise ValueError('Phone number can have only one + sign')
        
        # If has +, must be at start
        if '+' in v and not v.startswith('+'):
            raise ValueError('+ sign must be at the start of the phone number')
        
        # Extract digits only
        digits = re.sub(r'\D', '', clean_phone)
        
        # Check digit count (max 16)
        if len(digits) > 16:
            raise ValueError('Phone number too long (max 16 digits)')
        
        if len(digits) > 0 and len(digits) < 7:
            raise ValueError('Phone number too short (min 7 digits)')
        
        # Basic phone format check - flexible format with spaces, dashes, parentheses
        # Examples: +7 999 123-45-67, +44 20 7946 0958, (555) 123-4567
        phone_pattern = r'^\+?[1-9]\d{0,2}[\s\-]?\(?\d{1,4}\)?[\s\-\.]?\d{1,4}[\s\-\.]?\d{1,4}[\s\-\.]?\d{0,6}$'
        if v.strip() and not re.match(phone_pattern, v):
            raise ValueError('Invalid phone format')
        
        return v.strip()

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not v or not v.strip():
            return ""
        
        # RFC 5322 basic validation
        email_pattern = r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
        
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        
        # Check local part rules
        local_part = v.split('@')[0]
        
        # Cannot start or end with dot
        if local_part.startswith('.') or local_part.endswith('.'):
            raise ValueError('Email cannot start or end with a dot')
        
        # No consecutive dots
        if '..' in local_part:
            raise ValueError('Email cannot contain consecutive dots')
        
        # No disallowed characters
        disallowed = r'[<>()\[\]\\,"\s]'
        if re.search(disallowed, local_part):
            raise ValueError('Email contains invalid characters')
        
        return v.strip().lower()

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
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    comment: Optional[str] = None
    consent: bool
    created_at: datetime

    class Config:
        from_attributes = True