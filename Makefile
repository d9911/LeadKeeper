.PHONY: install dev backend frontend clean help

help: ## Показать справку
	@echo "LeadKeeper - Lead Capture Module"
	@echo ""
	@echo "Доступные команды:"
	@echo "  make install    Установить зависимости frontend и backend"
	@echo "  make dev        Запустить frontend и backend в режиме разработки"
	@echo "  make backend    Запустить только backend (FastAPI)"
	@echo "  make frontend   Запустить только frontend (Vite)"
	@echo "  make clean      Очистить временные файлы и кэш"

install: ## Установить зависимости
	@echo "==> Установка backend зависимостей..."
	@cd backend && pip install -r requirements.txt
	@echo ""
	@echo "==> Установка frontend зависимостей..."
	@cd frontend && npm install

dev: ## Запустить frontend и backend
	@echo "==> Запуск backend и frontend..."
	@echo "Backend будет доступен на http://localhost:8000"
	@echo "Frontend будет доступен на http://localhost:5173"
	@echo ""
	cd frontend && npm run dev &
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

backend: ## Запустить только backend
	@echo "==> Запуск backend на http://localhost:8000"
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend: ## Запустить только frontend
	@echo "==> Запуск frontend на http://localhost:5173"
	cd frontend && npm run dev

clean: ## Очистить временные файлы
	@echo "==> Очистка..."
	@find frontend -type d -name node_modules -exec rm -rf {} + 2>/dev/null || true
	@find frontend -type d -name dist -exec rm -rf {} + 2>/dev/null || true
	@find frontend -type d -name .vite -exec rm -rf {} + 2>/dev/null || true
	@rm -f backend/leadkeeper.db
	@echo "Готово"