"""
LeadKeeper - Lead Capture Module
FastAPI backend for lead form submissions

API Documentation: http://localhost:8000/docs (Swagger UI)
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
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LeadKeeper API",
    description="""
## LeadKeeper — Lead Capture Module API

Модуль для сбора и управления заявками с клиентских форм.

### Возможности
- Создание заявок с валидацией
- Просмотр списка заявок
- Email-уведомления владельцу и пользователю

### Валидация
- **Имя**: 2-100 символов, обязательно
- **Телефон**: формат +КодСтраны Номер, макс 16 цифр
- **Email**: RFC 5322 compliant
- **Хотя бы один контакт** (phone или email) обязателен
- **Согласие** на обработку данных обязательно
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS configuration for frontend
origins = [
    "http://localhost:5173",
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


@app.get(
    "/api/health",
    tags=["Health"],
    summary="Проверка работоспособности",
    description="Возвращает статус сервиса. Используйте для проверки доступности API."
)
def health_check():
    """
    Проверка здоровья сервиса.
    
    Returns:
        dict: Статус и название сервиса
    """
    return {"status": "ok", "service": "leadkeeper"}


@app.post(
    "/api/leads",
    response_model=LeadResponse,
    tags=["Leads"],
    summary="Создать новую заявку",
    description="""
Создаёт новую заявку в базе данных.

### Валидация
- `name`: Обязательно, 2-100 символов
- `phone`: Опционально, формат +КодСтраны Номер
- `email`: Опционально, RFC 5322
- Хотя бы `phone` или `email` должен быть заполнен
- `consent`: Обязательно, должен быть true

### Side Effects
- Отправляет email-уведомление владельцу (если настроено)
- Отправляет подтверждение пользователю (если email указан)
    """,
    responses={
        200: {"description": "Заявка успешно создана"},
        400: {"description": "Ошибка валидации данных"},
        422: {"description": "Некорректный формат данных"},
        500: {"description": "Внутренняя ошибка сервера"}
    }
)
def create_lead_endpoint(lead: LeadCreate):
    """
    Создание новой заявки.
    
    Args:
        lead: Данные заявки (LeadCreate schema)
    
    Returns:
        LeadResponse: Созданная заявка с ID и timestamp
    
    Raises:
        HTTPException: При ошибке валидации или внутренней ошибке
    """
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


@app.get(
    "/api/leads",
    response_model=list[LeadResponse],
    tags=["Leads"],
    summary="Получить список заявок",
    description="""
Возвращает список всех заявок, отсортированных по дате создания (новые первые).
    """,
    responses={
        200: {"description": "Список заявок"},
        500: {"description": "Внутренняя ошибка сервера"}
    }
)
def get_leads_endpoint():
    """
    Получение всех заявок.
    
    Returns:
        list[LeadResponse]: Список заявок
    """
    try:
        leads = get_leads()
        return leads
    except Exception as e:
        logger.error(f"Error getting leads: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get(
    "/api/leads/count",
    tags=["Leads"],
    summary="Количество заявок",
    description="Возвращает общее количество заявок в базе данных.",
    responses={
        200: {"description": "Количество заявок"},
        500: {"description": "Внутренняя ошибка сервера"}
    }
)
def get_leads_count():
    """
    Получение количества заявок.
    
    Returns:
        dict: Количество заявок
    """
    try:
        leads = get_leads()
        return {"count": len(leads)}
    except Exception as e:
        logger.error(f"Error getting leads count: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get(
    "/api/leads/{lead_id}",
    response_model=LeadResponse,
    tags=["Leads"],
    summary="Получить заявку по ID",
    description="Возвращает одну заявку по её идентификатору.",
    responses={
        200: {"description": "Заявка найдена"},
        404: {"description": "Заявка не найдена"},
        500: {"description": "Внутренняя ошибка сервера"}
    }
)
def get_lead_by_id(lead_id: int):
    """
    Получение заявки по ID.
    
    Args:
        lead_id: ID заявки
    
    Returns:
        LeadResponse: Заявка
    
    Raises:
        HTTPException: При ошибке
    """
    try:
        leads = get_leads()
        for lead in leads:
            if lead.id == lead_id:
                return lead
        raise HTTPException(status_code=404, detail="Lead not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting lead by id: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")