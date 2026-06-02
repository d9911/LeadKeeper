.PHONY: install install-backend install-frontend dev backend frontend clean clean-ports help check-python

PYTHON ?= python3.12
BACKEND_DIR = backend
FRONTEND_DIR = frontend
VENV = $(BACKEND_DIR)/.venv
PIP = $(VENV)/bin/pip
UVICORN = $(VENV)/bin/uvicorn
BACKEND_PORT = 8000
FRONTEND_PORT = 5173

help: ## Показать справку
	@echo "LeadKeeper - Lead Capture Module"
	@echo ""
	@echo "Доступные команды:"
	@echo "  make install           Установить frontend и backend зависимости"
	@echo "  make install-backend   Установить только backend зависимости через pip3 + venv"
	@echo "  make install-frontend  Установить только frontend зависимости через yarn"
	@echo "  make dev               Очистить порты и запустить frontend + backend"
	@echo "  make backend           Очистить backend порт и запустить только backend"
	@echo "  make frontend          Очистить frontend порт и запустить только frontend"
	@echo "  make clean-ports       Очистить порты backend и frontend"
	@echo "  make clean             Очистить зависимости, кэш и базу"

clean-ports: ## Очистить порты backend и frontend
	@echo "🧹 Очищаем порты $(BACKEND_PORT) и $(FRONTEND_PORT)..."
	-@npx --yes kill-port $(BACKEND_PORT) $(FRONTEND_PORT) > /dev/null 2>&1
	@echo "Порты очищены"

install: install-backend install-frontend ## Установить все зависимости

check-python:
	@$(PYTHON) -c "import sys; exit(0 if sys.version_info[:2] == (3, 12) else 1)" || \
	(echo "Ошибка: нужен Python 3.12. Сейчас используется: $$($(PYTHON) --version)"; exit 1)

# Пример:
# make install-backend PYTHON=/opt/homebrew/bin/python3.12
install-backend: check-python ## Установить backend зависимости в virtualenv
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

dev: clean-ports ## Очистить порты и запустить frontend + backend
	@test -d $(VENV) || (echo "Ошибка: backend зависимости не установлены. Запустите: make install-backend"; exit 1)
	@test -d $(FRONTEND_DIR)/node_modules || (echo "Ошибка: frontend зависимости не установлены. Запустите: make install-frontend"; exit 1)
	@echo "==> Запуск backend и frontend..."
	@echo "Backend будет доступен на http://localhost:$(BACKEND_PORT)"
	@echo "Frontend будет доступен на http://localhost:$(FRONTEND_PORT)"
	@echo ""
	cd $(FRONTEND_DIR) && yarn dev & \
	cd $(BACKEND_DIR) && .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port $(BACKEND_PORT)
		sleep 2 && xdg-open http://localhost:5173

backend: clean-ports ## Очистить порты и запустить только backend
	@test -d $(VENV) || (echo "Ошибка: backend зависимости не установлены. Запустите: make install-backend"; exit 1)
	@echo "==> Запуск backend на http://localhost:$(BACKEND_PORT)"
	cd $(BACKEND_DIR) && .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port $(BACKEND_PORT)

frontend: clean-ports ## Очистить порты и запустить только frontend
	@test -d $(FRONTEND_DIR)/node_modules || (echo "Ошибка: frontend зависимости не установлены. Запустите: make install-frontend"; exit 1)
	@echo "==> Запуск frontend на http://localhost:$(FRONTEND_PORT)"
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