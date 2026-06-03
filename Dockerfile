# ============================================
# LeadKeeper - Multi-stage Docker Build
# ============================================

# ---- Stage 1: Build Frontend ----
FROM node:20-alpine AS frontend-builder

WORKDIR /app

# Копируем только package.json для кэширования слоёв
COPY frontend/package*.json ./

# Устанавливаем зависимости
RUN npm ci --only=production=false

# Копируем весь frontend код
COPY frontend/ ./

# Билдим frontend (TypeScript + Vite)
RUN npm run build

# ---- Stage 2: Python Backend ----
FROM python:3.12-slim AS backend

# Переменные для оптимизации
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Устанавливаем системные зависимости для SMTP и других libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости backend
COPY backend/requirements.txt ./

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем backend код
COPY backend/ ./app/

# Копируем собранный frontend из Stage 1
COPY --from=frontend-builder /app/dist ./static

# Создаём директорию для данных
RUN mkdir -p /app/data

# ---- Stage 3: Final Runtime ----
FROM python:3.12-slim

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app

WORKDIR /app

# Устанавливаем только runtime зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Копируем всё из Stage 2
COPY --from=backend /app ./

# Создаём пользователя для безопасности (опционально)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Порт приложения
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]