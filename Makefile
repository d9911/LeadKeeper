.PHONY: install install-backend install-frontend dev backend frontend build build-frontend build-backend preview preview-full clean clean-ports clean-all help check-python check-node open-browser

# =========================
# LeadKeeper Makefile
# =========================

# Directories
BACKEND_DIR = backend
FRONTEND_DIR = frontend

# Python settings
PYTHON ?= python3.12
VENV = $(BACKEND_DIR)/.venv
PIP = $(VENV)/bin/pip
UVICORN = $(VENV)/bin/uvicorn

# Ports
BACKEND_PORT = 8000
FRONTEND_PORT = 5173
PREVIEW_PORT = 4173

# URLs
BACKEND_URL = http://localhost:$(BACKEND_PORT)
FRONTEND_URL = http://localhost:$(FRONTEND_PORT)
PREVIEW_URL = http://localhost:$(PREVIEW_PORT)
API_DOCS_URL = http://localhost:$(BACKEND_PORT)/docs

# Build output
DIST_DIR = $(FRONTEND_DIR)/dist

# Colors
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
CYAN := \033[0;36m
RED := \033[0;31m
BOLD := \033[1m
NC := \033[0m

help: ## Показать справку
	@echo ""
	@echo "$(BOLD)$(BLUE)LeadKeeper$(NC) — Lead Capture Module"
	@echo "$(CYAN)Мини-прототип lead-capture модуля для Alakris Platform$(NC)"
	@echo ""
	@echo "$(BOLD)🚀 Команды запуска:$(NC)"
	@echo "  $(GREEN)make install$(NC)        Установить все зависимости"
	@echo "  $(GREEN)make dev$(NC)            Запустить frontend + backend (режим разработки)"
	@echo "  $(GREEN)make backend$(NC)        Запустить только backend"
	@echo "  $(GREEN)make frontend$(NC)       Запустить только frontend"
	@echo ""
	@echo "$(BOLD)📦 Команды сборки:$(NC)"
	@echo "  $(GREEN)make build$(NC)          Полная сборка проекта (frontend + backend)"
	@echo "  $(GREEN)make build-frontend$(NC) Собрать только frontend (SSG)"
	@echo "  $(GREEN)make build-backend$(NC)  Собрать только backend"
	@echo "  $(GREEN)make preview$(NC)        Preview собранного frontend"
	@echo "  $(GREEN)make preview-full$(NC)   Preview frontend + запуск backend"
	@echo ""
	@echo "$(BOLD)🧹 Очистка:$(NC)"
	@echo "  $(GREEN)make clean$(NC)          Очистить кэш и временные файлы"
	@echo "  $(GREEN)make clean-all$(NC)      Полная очистка (зависимости + кэш)"
	@echo ""
	@echo "$(BOLD)🌐 URLs:$(NC)"
	@echo "  $(YELLOW)Frontend:$(NC)  $(FRONTEND_URL)"
	@echo "  $(YELLOW)Backend:$(NC)   $(BACKEND_URL)"
	@echo "  $(YELLOW)Preview:$(NC)   $(PREVIEW_URL)"
	@echo "  $(YELLOW)Swagger:$(NC)   $(API_DOCS_URL)"
	@echo ""

# =========================
# Installation
# =========================

install: install-backend install-frontend ## Установить все зависимости
	@echo ""
	@echo "$(GREEN)✅ Все зависимости установлены!$(NC)"
	@echo "Используйте: make dev"

install-backend: check-python ## Установить backend зависимости
	@echo ""
	@echo "$(BLUE)🐍 Backend setup$(NC)"
	@echo "$(YELLOW)==> Создаём Python virtualenv...$(NC)"
	@cd $(BACKEND_DIR) && $(PYTHON) -m venv .venv
	@echo "$(YELLOW)==> Обновляем pip...$(NC)"
	@$(PIP) install --upgrade pip
	@echo "$(YELLOW)==> Устанавливаем зависимости...$(NC)"
	@$(PIP) install -r $(BACKEND_DIR)/requirements.txt
	@echo "$(GREEN)✅ Backend готов!$(NC)"

install-frontend: check-node ## Установить frontend зависимости
	@echo ""
	@echo "$(BLUE)⚛️  Frontend setup$(NC)"
	@cd $(FRONTEND_DIR) && npm install
	@echo "$(GREEN)✅ Frontend готов!$(NC)"

# =========================
# Development
# =========================

check-python:
	@$(PYTHON) --version | grep -q "Python 3.1[0-9]" || \
		(echo "$(RED)⚠️  Рекомендуется Python 3.10+. Текущая:"; $(PYTHON) --version; echo "")

check-node:
	@node --version | grep -q "v1[89]\|v2[0-9]" || \
		(echo "$(YELLOW)⚠️  Рекомендуется Node 18+. Текущая:"; node --version; echo "")

clean-ports: ## Очистить порты
	@echo "$(YELLOW)🧹 Очищаем порты...$(NC)"
	@-lsof -ti :$(BACKEND_PORT) | xargs kill -9 2>/dev/null || true
	@-lsof -ti :$(FRONTEND_PORT) | xargs kill -9 2>/dev/null || true
	@-lsof -ti :$(PREVIEW_PORT) | xargs kill -9 2>/dev/null || true
	@echo "$(GREEN)✅ Порты свободны$(NC)"

open-browser:
	@sleep 2 && open $(FRONTEND_URL) >/dev/null 2>&1 || true

open-preview:
	@sleep 2 && open $(PREVIEW_URL) >/dev/null 2>&1 || true

dev: clean-ports ## Запустить frontend + backend (режим разработки)
	@test -d $(VENV) || (echo "$(RED)❌ Запустите: make install-backend$(NC)"; exit 1)
	@test -d $(FRONTEND_DIR)/node_modules || (echo "$(RED)❌ Запустите: make install-frontend$(NC)"; exit 1)
	@echo ""
	@echo "$(BLUE)🚀 LeadKeeper (dev mode)$(NC)"
	@echo "$(YELLOW)Frontend:$(NC) $(FRONTEND_URL)"
	@echo "$(YELLOW)Backend:$(NC)  $(BACKEND_URL)"
	@echo "$(YELLOW)Swagger:$(NC)  $(API_DOCS_URL)"
	@echo ""
	@$(MAKE) open-browser &
	@cd $(FRONTEND_DIR) && npm run dev &
	@cd $(BACKEND_DIR) && .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port $(BACKEND_PORT)

backend: clean-ports ## Запустить только backend
	@test -d $(VENV) || (echo "$(RED)❌ Запустите: make install-backend$(NC)"; exit 1)
	@echo ""
	@echo "$(BLUE)🚀 Backend$(NC)"
	@echo "$(YELLOW)API:$(NC)   $(BACKEND_URL)"
	@echo "$(YELLOW)Docs:$(NC)  $(API_DOCS_URL)"
	@echo ""
	@cd $(BACKEND_DIR) && .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port $(BACKEND_PORT)

frontend: clean-ports ## Запустить только frontend
	@test -d $(FRONTEND_DIR)/node_modules || (echo "$(RED)❌ Запустите: make install-frontend$(NC)"; exit 1)
	@echo ""
	@echo "$(BLUE)🚀 Frontend$(NC)"
	@echo "$(YELLOW)URL:$(NC) $(FRONTEND_URL)"
	@echo ""
	@$(MAKE) open-browser &
	@cd $(FRONTEND_DIR) && npm run dev

# =========================
# Build (SSG)
# =========================

build: build-frontend build-backend ## Полная сборка проекта
	@echo ""
	@echo "$(GREEN)✅ LeadKeeper собран!$(NC)"
	@echo ""
	@echo "Статика: $(DIST_DIR)"
	@echo ""
	@echo "Для preview: make preview-full"
	@echo "Для деплоя: скопируйте $(DIST_DIR) на хостинг"

build-frontend: ## Собрать frontend (SSG/pre-rendering)
	@test -d $(FRONTEND_DIR)/node_modules || (echo "$(RED)❌ Запустите: make install-frontend$(NC)"; exit 1)
	@echo ""
	@echo "$(BLUE)📦 Сборка frontend (SSG)$(NC)"
	@echo "$(YELLOW)==> Очищаем старый билд...$(NC)"
	@rm -rf $(DIST_DIR)
	@echo "$(YELLOW)==> Компилируем TypeScript...$(NC)"
	@cd $(FRONTEND_DIR) && npx tsc --noEmit || (echo "$(RED)❌ TypeScript errors!$(NC)"; exit 1)
	@echo "$(YELLOW)==> Билдим...$(NC)"
	@cd $(FRONTEND_DIR) && npm run build
	@echo ""
	@ls -la $(DIST_DIR)
	@echo "$(GREEN)✅ Frontend собран!$(NC)"

build-backend: ## Собрать backend
	@test -d $(VENV) || (echo "$(RED)❌ Запустите: make install-backend$(NC)"; exit 1)
	@echo ""
	@echo "$(BLUE)📦 Проверка backend...$(NC)"
	@cd $(BACKEND_DIR) && .venv/bin/python -c "from app.main import app; print('✅ Backend OK')"
	@echo "$(GREEN)✅ Backend проверен!$(NC)"

# =========================
# Preview
# =========================

preview: clean-ports ## Preview собранного frontend
	@test -d $(DIST_DIR) || (echo "$(RED)❌ Сначала: make build-frontend$(NC)"; exit 1)
	@echo ""
	@echo "$(BLUE)👁️  Preview$(NC)"
	@echo "$(YELLOW)URL:$(NC) $(PREVIEW_URL)"
	@echo ""
	@$(MAKE) open-preview &
	@cd $(FRONTEND_DIR) && npm run preview

preview-full: clean-ports build ## Preview frontend + запуск backend !!!!!!!!!!!!!!!!
	@echo ""
	@echo "$(BLUE)🚀 Full Preview Mode$(NC)"
	@echo "$(YELLOW)Frontend:$(NC) $(PREVIEW_URL)"
	@echo "$(YELLOW)Backend:$(NC)  $(BACKEND_URL)"
	@echo ""
	@$(MAKE) open-preview &
	@cd $(FRONTEND_DIR) && npm run preview &
	@cd $(BACKEND_DIR) && .venv/bin/uvicorn app.main:app --host 0.0.0.0 --port $(BACKEND_PORT)

# всё работает в одной команде если стоит node 20 и python3.12
i: install preview-full
# =========================
# Cleanup
# =========================

clean: ## Очистить кэш и временные файлы
	@echo ""
	@echo "$(YELLOW)🧹 Очищаем кэш...$(NC)"
	@find $(BACKEND_DIR) -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find $(BACKEND_DIR) -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find $(BACKEND_DIR) -type f -name "*.pyc" -delete 2>/dev/null || true
	@rm -f $(BACKEND_DIR)/leadkeeper.db
	@rm -rf $(FRONTEND_DIR)/.vite
	@rm -rf $(FRONTEND_DIR)/dist
	@echo "$(GREEN)✅ Кэш очищен$(NC)"

clean-all: clean-ports clean ## Полная очистка (включая зависимости)
	@echo ""
	@echo "$(YELLOW)🧹 Полная очистка...$(NC)"
	@rm -rf $(BACKEND_DIR)/.venv
	@rm -rf $(FRONTEND_DIR)/node_modules
	@rm -rf $(FRONTEND_DIR)/.yarn 2>/dev/null || true
	@rm -rf $(FRONTEND_DIR)/dist
	@rm -rf $(FRONTEND_DIR)/.vite
	@echo "$(GREEN)✅ Проект очищен$(NC)"