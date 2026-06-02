.PHONY: install install-backend install-frontend dev backend frontend clean clean-ports help check-python open-browser

# =========================
# LeadKeeper Makefile
# =========================

PYTHON ?= python3.12

BACKEND_DIR = backend
FRONTEND_DIR = frontend

VENV = $(BACKEND_DIR)/.venv
PIP = $(VENV)/bin/pip
UVICORN = $(VENV)/bin/uvicorn

BACKEND_PORT = 8000
FRONTEND_PORT = 5173

BACKEND_URL = http://localhost:$(BACKEND_PORT)
FRONTEND_URL = http://localhost:$(FRONTEND_PORT)
API_DOCS_URL = http://localhost:$(BACKEND_PORT)/docs

# Colors
GREEN = \033[0;32m
YELLOW = \033[0;33m
BLUE = \033[0;34m
CYAN = \033[0;36m
RED = \033[0;31m
BOLD = \033[1m
NC = \033[0m

help: ## Показать справку
	@echo ""
	@echo "$(BOLD)$(BLUE)LeadKeeper$(NC) — Lead Capture Module"
	@echo "$(CYAN)Мини-прототип lead-capture модуля для Alakris Platform$(NC)"
	@echo ""
	@echo "$(BOLD)Доступные команды:$(NC)"
	@echo "  $(GREEN)make install$(NC)           Установить frontend и backend зависимости"
	@echo "  $(GREEN)make install-backend$(NC)   Установить только backend зависимости через Python venv"
	@echo "  $(GREEN)make install-frontend$(NC)  Установить только frontend зависимости через yarn"
	@echo "  $(GREEN)make dev$(NC)               Очистить порты и запустить frontend + backend"
	@echo "  $(GREEN)make backend$(NC)           Очистить порты и запустить только backend FastAPI"
	@echo "  $(GREEN)make frontend$(NC)          Очистить порты и запустить только frontend Vite"
	@echo "  $(GREEN)make clean-ports$(NC)       Очистить порты backend и frontend"
	@echo "  $(GREEN)make clean$(NC)             Очистить зависимости, кэш и локальную базу"
	@echo ""
	@echo "$(BOLD)URL:$(NC)"
	@echo "  $(YELLOW)Frontend:$(NC) $(FRONTEND_URL)"
	@echo "  $(YELLOW)Backend:$(NC)  $(BACKEND_URL)"
	@echo "  $(YELLOW)Swagger:$(NC)  $(API_DOCS_URL)"
	@echo ""

install: install-backend install-frontend ## Установить все зависимости
	@echo ""
	@echo "$(GREEN)✅ Все зависимости установлены$(NC)"

check-python:
	@$(PYTHON) -c "import sys; exit(0 if sys.version_info[:2] == (3, 12) else 1)" || \
	(echo "$(RED)❌ Ошибка: нужен Python 3.12. Сейчас используется: $$($(PYTHON) --version)$(NC)"; exit 1)

install-backend: check-python ## Установить backend зависимости в virtualenv
	@echo ""
	@echo "$(BLUE)🐍 Backend setup$(NC)"
	@echo "$(YELLOW)==> Создаём Python virtualenv...$(NC)"
	@cd $(BACKEND_DIR) && $(PYTHON) -m venv .venv
	@echo ""
	@echo "$(YELLOW)==> Обновляем pip...$(NC)"
	@$(PIP) install --upgrade pip
	@echo ""
	@echo "$(YELLOW)==> Устанавливаем backend зависимости...$(NC)"
	@$(PIP) install -r $(BACKEND_DIR)/requirements.txt
	@echo "$(GREEN)✅ Backend зависимости установлены$(NC)"

install-frontend: ## Установить frontend зависимости через yarn
	@echo ""
	@echo "$(BLUE)⚛️  Frontend setup$(NC)"
	@echo "$(YELLOW)==> Устанавливаем frontend зависимости...$(NC)"
	@cd $(FRONTEND_DIR) && yarn install
	@echo "$(GREEN)✅ Frontend зависимости установлены$(NC)"

clean-ports: ## Очистить порты backend и frontend
	@echo ""
	@echo "$(YELLOW)🧹 Очищаем порты $(BACKEND_PORT) и $(FRONTEND_PORT)...$(NC)"
	-@npx --yes kill-port $(BACKEND_PORT) $(FRONTEND_PORT) > /dev/null 2>&1
	@echo "$(GREEN)✅ Порты очищены$(NC)"

open-browser:
	@sleep 2 && open $(FRONTEND_URL) >/dev/null 2>&1 || true

dev: clean-ports ## Очистить порты и запустить frontend + backend
	@test -d $(VENV) || (echo "$(RED)❌ Backend зависимости не установлены. Запустите: make install-backend$(NC)"; exit 1)
	@test -d $(FRONTEND_DIR)/node_modules || (echo "$(RED)❌ Frontend зависимости не установлены. Запустите: make install-frontend$(NC)"; exit 1)
	@echo ""
	@echo "$(BLUE)🚀 Запускаем LeadKeeper$(NC)"
	@echo "$(YELLOW)Backend:$(NC)  $(BACKEND_URL)"
	@echo "$(YELLOW)Frontend:$(NC) $(FRONTEND_URL)"
	@echo "$(YELLOW)Swagger:$(NC)  $(API_DOCS_URL)"
	@echo ""
	@$(MAKE) open-browser &
	cd $(FRONTEND_DIR) && yarn dev & \
	cd $(BACKEND_DIR) && .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port $(BACKEND_PORT)

backend: clean-ports ## Очистить порты и запустить только backend
	@test -d $(VENV) || (echo "$(RED)❌ Backend зависимости не установлены. Запустите: make install-backend$(NC)"; exit 1)
	@echo ""
	@echo "$(BLUE)🚀 Запускаем backend$(NC)"
	@echo "$(YELLOW)Backend:$(NC) $(BACKEND_URL)"
	@echo "$(YELLOW)Swagger:$(NC) $(API_DOCS_URL)"
	@echo ""
	cd $(BACKEND_DIR) && .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port $(BACKEND_PORT)

frontend: clean-ports ## Очистить порты и запустить только frontend
	@test -d $(FRONTEND_DIR)/node_modules || (echo "$(RED)❌ Frontend зависимости не установлены. Запустите: make install-frontend$(NC)"; exit 1)
	@echo ""
	@echo "$(BLUE)🚀 Запускаем frontend$(NC)"
	@echo "$(YELLOW)Frontend:$(NC) $(FRONTEND_URL)"
	@echo ""
	@$(MAKE) open-browser &
	cd $(FRONTEND_DIR) && yarn dev

clean: ## Очистить временные файлы
	@echo ""
	@echo "$(YELLOW)🧹 Очищаем проект...$(NC)"
	@rm -rf $(BACKEND_DIR)/.venv
	@rm -f $(BACKEND_DIR)/leadkeeper.db
	@find $(BACKEND_DIR) -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find $(BACKEND_DIR) -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf $(FRONTEND_DIR)/node_modules
	@rm -rf $(FRONTEND_DIR)/dist
	@rm -rf $(FRONTEND_DIR)/.vite
	@echo "$(GREEN)✅ Готово$(NC)"