
# ---- Stage 1: Build Frontend ----
FROM node:20-alpine AS frontend-builder

WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# ---- Stage 2: Final Runtime ----
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Устанавливаем зависимости
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем backend структуру: backend/app/...
COPY backend/ ./backend/

# Копируем статику
COPY --from=frontend-builder /app/dist ./frontend/dist

# Директория для данных
RUN mkdir -p /app/data

# PORT
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1

# ЗАПУСК: меняем рабочую директорию на backend и запускаем как в Makefile
# Makefile: cd backend && .venv/bin/uvicorn app.main:app
WORKDIR /app/backend
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]