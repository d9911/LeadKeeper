.PHONY: install install-backend install-frontend dev backend frontend clean help

PYTHON = python3
BACKEND_DIR = backend
FRONTEND_DIR = frontend
VENV = $(BACKEND_DIR)/.venv
PIP = $(VENV)/bin/pip
UVICORN = $(VENV)/bin/uvicorn

help: ## Показать справку
	@echo "LeadKeeper - Lead Capture Module"
	@echo ""
	@echo "Доступные команды:"
	@echo "  make install           Установить frontend и backend зависимости"
	@echo "  make install-backend   Установить только backend зависимости через pip3 + venv"
	@echo "  make install-frontend  Установить только frontend зависимости через yarn"
	@echo "  make dev               Запустить frontend и backend"
	@echo "  make backend           Запустить только backend FastAPI"
	@echo "  make frontend          Запустить только frontend Vite"
	@echo "  make clean             Очистить временные файлы и кэш"

install: install-backend install-frontend ## Установить все зависимости

install-backend: ## Установить backend зависимости через pip3 в virtualenv
	@echo "==> Создание Python virtualenv..."
	@cd $(BACKEND_DIR) && $(PYTHON) -m venv .venv
	@echo ""
	@echo "==> Обновление pip..."
	@$(PIP) install --upgrade pip
	@echo ""
	@echo "==> Установка backend зависимостей..."
	@$(PIP) install -r $(BACKEND_DIR)/requirements.txt

install-frontend: ## Установить frontend зависимости через yarn
	@echo "==> Установка frontend зависимостей..."
	@cd $(FRONTEND_DIR) && yarn install

dev: ## Запустить frontend и backend
	@echo "==> Запуск backend и frontend..."
	@echo "Backend будет доступен на http://localhost:8000"
	@echo "Frontend будет доступен на http://localhost:5173"
	@echo ""
	cd $(FRONTEND_DIR) && yarn dev & \
	cd $(BACKEND_DIR) && .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

backend: ## Запустить только backend
	@echo "==> Запуск backend на http://localhost:8000"
	cd $(BACKEND_DIR) && .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend: ## Запустить только frontend
	@echo "==> Запуск frontend на http://localhost:5173"
	cd $(FRONTEND_DIR) && yarn dev

clean: ## Очистить временные файлы
	@echo "==> Очистка..."
	@rm -rf $(BACKEND_DIR)/.venv
	@rm -f $(BACKEND_DIR)/leadkeeper.db
	@find $(BACKEND_DIR) -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find $(BACKEND_DIR) -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf $(FRONTEND_DIR)/node_modules
	@rm -rf $(FRONTEND_DIR)/dist
	@rm -rf $(FRONTEND_DIR)/.vite
	@echo "Готово"