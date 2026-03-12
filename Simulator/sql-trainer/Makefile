# ══════════════════════════════════════════════════════════════════════════════
#  SQL Trainer — Makefile
#  Использование: make <target>
# ══════════════════════════════════════════════════════════════════════════════

PYTHON      := python3
PIP         := $(PYTHON) -m pip
VENV        := backend/.venv
VENV_BIN    := $(VENV)/bin
PYTEST      := $(VENV_BIN)/pytest
UVICORN     := $(VENV_BIN)/uvicorn

BACKEND_DIR := backend
FRONTEND_DIR := frontend

# Цвета для вывода
CYAN  := \033[0;36m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED   := \033[0;31m
RESET := \033[0m

.DEFAULT_GOAL := help

# ── Help ──────────────────────────────────────────────────────────────────────
.PHONY: help
help:
	@echo ""
	@echo "$(CYAN)SQL Trainer$(RESET) — команды управления проектом"
	@echo ""
	@echo "$(YELLOW)Быстрый старт:$(RESET)"
	@echo "  make setup        Установить все зависимости (backend + frontend)"
	@echo "  make up           Запустить всё через Docker Compose"
	@echo "  make dev          Запустить backend и frontend локально (без Docker)"
	@echo ""
	@echo "$(YELLOW)Разработка:$(RESET)"
	@echo "  make backend-dev  Запустить только backend (uvicorn --reload)"
	@echo "  make frontend-dev Запустить только frontend (vite dev)"
	@echo "  make db-up        Поднять только PostgreSQL + Redis в Docker"
	@echo "  make db-down      Остановить базы данных"
	@echo ""
	@echo "$(YELLOW)Тестирование:$(RESET)"
	@echo "  make test         Запустить все тесты"
	@echo "  make test-backend Тесты только backend (pytest)"
	@echo "  make test-types   Проверка TypeScript типов (tsc --noEmit)"
	@echo "  make lint         Линтер frontend (eslint)"
	@echo ""
	@echo "$(YELLOW)Docker:$(RESET)"
	@echo "  make up           Поднять весь стек (build + start)"
	@echo "  make down         Остановить и удалить контейнеры"
	@echo "  make restart      Пересобрать и перезапустить"
	@echo "  make logs         Показать логи всех сервисов"
	@echo "  make logs-backend Показать логи backend"
	@echo ""
	@echo "$(YELLOW)Утилиты:$(RESET)"
	@echo "  make clean        Удалить артефакты сборки и кэши"
	@echo "  make env          Создать .env файл из .env.example"
	@echo "  make api-docs     Открыть Swagger UI в браузере"
	@echo ""

# ── Setup ─────────────────────────────────────────────────────────────────────
.PHONY: setup setup-backend setup-frontend env

setup: setup-backend setup-frontend
	@echo "$(GREEN)✓ Все зависимости установлены$(RESET)"

setup-backend:
	@echo "$(CYAN)→ Устанавливаем зависимости backend...$(RESET)"
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip -q
	$(VENV)/bin/pip install -r $(BACKEND_DIR)/requirements.txt -q
	@echo "$(GREEN)✓ Backend готов$(RESET)"

setup-frontend:
	@echo "$(CYAN)→ Устанавливаем зависимости frontend...$(RESET)"
	cd $(FRONTEND_DIR) && npm install --silent
	@echo "$(GREEN)✓ Frontend готов$(RESET)"

env:
	@if [ ! -f $(BACKEND_DIR)/.env ]; then \
		cp $(BACKEND_DIR)/.env.example $(BACKEND_DIR)/.env; \
		echo "$(GREEN)✓ Создан $(BACKEND_DIR)/.env из .env.example$(RESET)"; \
	else \
		echo "$(YELLOW)! $(BACKEND_DIR)/.env уже существует, пропускаем$(RESET)"; \
	fi

# ── Docker ────────────────────────────────────────────────────────────────────
.PHONY: up down restart logs logs-backend db-up db-down

up:
	@echo "$(CYAN)→ Запуск полного стека через Docker Compose...$(RESET)"
	docker compose up --build -d
	@echo ""
	@echo "$(GREEN)✓ Сервисы запущены:$(RESET)"
	@echo "  Frontend  → http://localhost:3000"
	@echo "  Backend   → http://localhost:8000"
	@echo "  Swagger   → http://localhost:8000/docs"
	@echo ""
	@echo "Демо-аккаунт преподавателя: teacher@example.com / teacher123"

down:
	@echo "$(CYAN)→ Останавливаем контейнеры...$(RESET)"
	docker compose down
	@echo "$(GREEN)✓ Контейнеры остановлены$(RESET)"

restart:
	@echo "$(CYAN)→ Пересборка и перезапуск...$(RESET)"
	docker compose down
	docker compose up --build -d
	@echo "$(GREEN)✓ Перезапущено$(RESET)"

logs:
	docker compose logs -f

logs-backend:
	docker compose logs -f backend

db-up:
	@echo "$(CYAN)→ Запуск PostgreSQL и Redis...$(RESET)"
	docker compose up -d postgres redis
	@echo "$(GREEN)✓ БД запущена на localhost:5432, Redis на localhost:6379$(RESET)"

db-down:
	docker compose stop postgres redis

# ── Локальная разработка ──────────────────────────────────────────────────────
.PHONY: dev backend-dev frontend-dev

dev: db-up
	@echo "$(CYAN)→ Запуск backend и frontend в фоне...$(RESET)"
	@echo "$(YELLOW)Для остановки: make down + закройте процессы$(RESET)"
	$(MAKE) -j2 backend-dev frontend-dev

backend-dev: env
	@echo "$(CYAN)→ Backend: http://localhost:8000$(RESET)"
	cd $(BACKEND_DIR) && .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend-dev:
	@echo "$(CYAN)→ Frontend: http://localhost:3000$(RESET)"
	cd $(FRONTEND_DIR) && npm run dev

# ── Тесты ─────────────────────────────────────────────────────────────────────
.PHONY: test test-backend test-types lint

test: test-backend test-types
	@echo ""
	@echo "$(GREEN)✓ Все проверки пройдены$(RESET)"

test-backend:
	@echo "$(CYAN)→ Запуск pytest (backend)...$(RESET)"
	@if [ ! -d $(VENV) ]; then $(MAKE) setup-backend; fi
	cd $(BACKEND_DIR) && .venv/bin/pytest app/tests/ -v --tb=short
	@echo "$(GREEN)✓ Backend тесты пройдены$(RESET)"

test-backend-cov:
	@echo "$(CYAN)→ Pytest с покрытием...$(RESET)"
	@if [ ! -d $(VENV) ]; then $(MAKE) setup-backend; fi
	cd $(BACKEND_DIR) && .venv/bin/pytest app/tests/ -v --tb=short \
		--cov=app --cov-report=term-missing --cov-report=html:htmlcov
	@echo "$(GREEN)✓ Отчёт покрытия: backend/htmlcov/index.html$(RESET)"

test-types:
	@echo "$(CYAN)→ Проверка TypeScript типов...$(RESET)"
	cd $(FRONTEND_DIR) && npx tsc --noEmit
	@echo "$(GREEN)✓ TypeScript типы корректны$(RESET)"

lint:
	@echo "$(CYAN)→ ESLint (frontend)...$(RESET)"
	cd $(FRONTEND_DIR) && npm run lint
	@echo "$(GREEN)✓ Линтер пройден$(RESET)"

# ── Сборка ────────────────────────────────────────────────────────────────────
.PHONY: build build-frontend

build: build-frontend
	@echo "$(GREEN)✓ Сборка завершена$(RESET)"

build-frontend:
	@echo "$(CYAN)→ Сборка frontend (production)...$(RESET)"
	cd $(FRONTEND_DIR) && npm run build
	@echo "$(GREEN)✓ Frontend собран: frontend/dist/$(RESET)"

# ── Утилиты ───────────────────────────────────────────────────────────────────
.PHONY: clean api-docs check-deps

clean:
	@echo "$(CYAN)→ Очистка артефактов...$(RESET)"
	rm -rf $(FRONTEND_DIR)/dist
	rm -rf $(FRONTEND_DIR)/node_modules/.cache
	find $(BACKEND_DIR) -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; true
	find $(BACKEND_DIR) -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null; true
	find $(BACKEND_DIR) -type d -name htmlcov -exec rm -rf {} + 2>/dev/null; true
	find $(BACKEND_DIR) -name "*.pyc" -delete 2>/dev/null; true
	@echo "$(GREEN)✓ Очищено$(RESET)"

clean-all: clean
	@echo "$(CYAN)→ Удаление venv и node_modules...$(RESET)"
	rm -rf $(VENV)
	rm -rf $(FRONTEND_DIR)/node_modules
	@echo "$(GREEN)✓ Полная очистка завершена$(RESET)"

api-docs:
	@echo "$(CYAN)→ Открываем Swagger UI...$(RESET)"
	open http://localhost:8000/docs 2>/dev/null || xdg-open http://localhost:8000/docs

check-deps:
	@echo "$(CYAN)→ Проверка системных зависимостей...$(RESET)"
	@command -v $(PYTHON) >/dev/null 2>&1 && echo "$(GREEN)✓ python3$(RESET)" || echo "$(RED)✗ python3 не найден$(RESET)"
	@command -v node    >/dev/null 2>&1 && echo "$(GREEN)✓ node $(shell node -v)$(RESET)" || echo "$(RED)✗ node не найден$(RESET)"
	@command -v npm     >/dev/null 2>&1 && echo "$(GREEN)✓ npm $(shell npm -v)$(RESET)"  || echo "$(RED)✗ npm не найден$(RESET)"
	@command -v docker  >/dev/null 2>&1 && echo "$(GREEN)✓ docker$(RESET)" || echo "$(RED)✗ docker не найден$(RESET)"
	@command -v docker  >/dev/null 2>&1 && docker compose version >/dev/null 2>&1 && echo "$(GREEN)✓ docker compose$(RESET)" || echo "$(RED)✗ docker compose не найден$(RESET)"
