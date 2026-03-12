# SQL Trainer

Интерактивный тренажёр SQL для студентов с веб-интерфейсом, системой заданий и автоматической проверкой решений.

## Содержание

- [Возможности](#возможности)
- [Архитектура](#архитектура)
- [Быстрый старт](#быстрый-старт)
- [Разработка](#разработка)
- [Тестирование](#тестирование)
- [API](#api)
- [Структура проекта](#структура-проекта)

---

## Возможности

### Для студентов

- SQL-редактор с подсветкой синтаксиса (Monaco Editor / VS Code engine)
- Мгновенное выполнение запросов в изолированной sandbox-среде
- Проверка решения с детальным diff — видно какие строки лишние или отсутствуют
- Подсказки к каждому заданию
- Просмотр схемы базы данных задания прямо в интерфейсе
- Прогресс по всем заданиям с счётчиком попыток

### Для преподавателей

- Панель управления заданиями (создание, удаление, просмотр)
- Форма создания задания с тремя SQL-редакторами (схема, данные, эталон)
- Тест схемы и эталонного решения прямо в форме до сохранения
- Превью схемы таблиц из DDL в реальном времени

### Безопасность sandbox

- Разрешены только `SELECT` и `WITH ... SELECT` (CTE)
- Блокировка `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER` и др.
- Таймаут выполнения — 5 секунд
- Лимит результата — 500 строк
- Полная изоляция: каждый запрос выполняется в отдельной in-memory SQLite БД

---

## Архитектура

```text
┌─────────────────┐     HTTP/JSON      ┌──────────────────────┐
│   Frontend      │ ◄────────────────► │   Backend (FastAPI)  │
│  React + Vite   │                    │                      │
│  TypeScript     │                    │  ┌────────────────┐  │
│  Monaco Editor  │                    │  │  SQL Executor  │  │
│  TanStack Query │                    │  │  (SQLite mem)  │  │
│  Zustand        │                    │  └────────────────┘  │
│  Tailwind CSS   │                    │  ┌────────────────┐  │
└─────────────────┘                    │  │  Comparator    │  │
                                       │  └────────────────┘  │
                                       │         │            │
                                       │  ┌──────▼───────┐   │
                                       │  │  PostgreSQL   │   │
                                       │  └──────────────┘   │
                                       └──────────────────────┘
```

### Стек

| Слой | Технология |
| --- | --- |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS 4 |
| UI компоненты | Monaco Editor, TanStack Table, TanStack Query, Zustand |
| Backend | FastAPI (Python 3.12), SQLAlchemy 2.0 async |
| SQL Sandbox | SQLite in-memory (stdlib) |
| База данных | PostgreSQL 16 |
| Кэш | Redis 7 |
| Контейнеры | Docker, Docker Compose |

---

## Быстрый старт

### Вариант 1 — Docker Compose (рекомендуется)

Требования: Docker, Docker Compose v2

```bash
git clone <repo-url>
cd sql-trainer

# Поднять весь стек одной командой
make up
```

Сервисы будут доступны:

| Сервис | URL |
| --- | --- |
| Frontend | <http://localhost:3000> |
| Backend API | <http://localhost:8000> |
| Swagger UI | <http://localhost:8000/docs> |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |

Демо-аккаунты (создаются автоматически при первом запуске):

| Роль | Email | Пароль |
| --- | --- | --- |
| Преподаватель | teacher@example.com | teacher123 |

Студент регистрируется самостоятельно через форму входа.

### Вариант 2 — Локальная разработка

Требования: Python 3.11+, Node.js 18+, Docker (только для БД)

```bash
# 1. Установить зависимости
make setup

# 2. Создать .env файл
make env

# 3. Запустить PostgreSQL и Redis в Docker
make db-up

# 4. Запустить backend и frontend в разных терминалах
make backend-dev   # → http://localhost:8000
make frontend-dev  # → http://localhost:3000
```

---

## Разработка

### Команды Makefile

```bash
make help             # Показать все доступные команды

# Быстрый старт
make setup            # Установить все зависимости
make up               # Запустить через Docker Compose
make down             # Остановить контейнеры

# Локальная разработка
make db-up            # Только PostgreSQL + Redis
make backend-dev      # Backend с hot-reload
make frontend-dev     # Frontend с hot-reload (HMR)

# Тесты
make test             # Все проверки (pytest + tsc)
make test-backend     # Только backend тесты (pytest)
make test-backend-cov # Pytest с отчётом покрытия
make test-types       # Проверка TypeScript типов
make lint             # ESLint для frontend

# Дополнительно
make build            # Production сборка frontend
make clean            # Удалить кэши и артефакты
make api-docs         # Открыть Swagger UI в браузере
make check-deps       # Проверить системные зависимости
```

### Переменные окружения (backend/.env)

```env
# База данных
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/sql_trainer

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT — обязательно сменить в production
SECRET_KEY=your-secret-key-here

# Режим отладки
DEBUG=true

# Лимиты sandbox (опционально)
SANDBOX_TIMEOUT_SEC=5
SANDBOX_MAX_ROWS=500
```

### Добавление заданий через API

```bash
# Получить токен преподавателя
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"teacher@example.com","password":"teacher123"}' \
  | jq -r '.access_token')

# Создать задание
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Выбрать активных пользователей",
    "description": "Верните `id` и `name` пользователей где `active = 1`.",
    "difficulty": "easy",
    "topic": "WHERE",
    "order_num": 10,
    "reference_sql": "SELECT id, name FROM users WHERE active = 1",
    "db_schema_sql": "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, active INTEGER);",
    "db_seed_sql": "INSERT INTO users VALUES (1,'\''Алиса'\'',1),(2,'\''Боб'\'',0);",
    "order_matters": false,
    "hints": ["Используйте WHERE active = 1"]
  }'
```

---

## Тестирование

### Backend (pytest)

```bash
make test-backend
```

Тесты покрывают:

- `TestQueryValidator` — блокировка DDL/DML, валидация SELECT, CTE
- `TestSQLExecutor` — выполнение запросов, обработка ошибок, таймаут
- `TestResultComparator` — точное совпадение, порядок строк, diff, дубликаты

```text
app/tests/
├── test_executor.py    # 12 тестов: QueryValidator + SQLExecutor
└── test_comparator.py  # 7 тестов: ResultComparator
```

Запуск с отчётом покрытия:

```bash
make test-backend-cov
# Отчёт: backend/htmlcov/index.html
```

### Frontend (TypeScript)

```bash
make test-types   # tsc --noEmit
make lint         # ESLint
```

---

## API

Полная документация доступна по адресу **<http://localhost:8000/docs>** (Swagger UI).

### Эндпоинты

| Метод | URL | Описание | Роль |
| --- | --- | --- | --- |
| POST | `/api/auth/register` | Регистрация | — |
| POST | `/api/auth/login` | Вход, получение JWT | — |
| GET | `/api/tasks` | Список заданий | student, teacher |
| GET | `/api/tasks/{id}` | Задание + схема БД | student, teacher |
| POST | `/api/tasks` | Создать задание | teacher |
| DELETE | `/api/tasks/{id}` | Удалить задание | teacher |
| POST | `/api/execute` | Выполнить SQL-запрос | student, teacher |
| POST | `/api/validate` | Проверить решение | student, teacher |
| GET | `/api/progress` | Прогресс текущего пользователя | student, teacher |
| GET | `/api/progress/leaderboard` | Таблица лидеров | student, teacher |
| POST | `/api/teacher/sandbox` | Тест SQL без сохранения задачи | teacher |
| GET | `/api/health` | Проверка работоспособности | — |

### Формат ответа `/api/execute`

```json
{
  "success": true,
  "result": {
    "columns": ["id", "name", "amount"],
    "rows": [[1, "Алиса", 150.0], [2, "Боб", 200.0]],
    "row_count": 2
  },
  "error": null
}
```

### Формат ответа `/api/validate`

```json
{
  "is_correct": false,
  "student_result": { "columns": ["id"], "rows": [[1]], "row_count": 1 },
  "error": null,
  "diff": [
    { "row": [2, "Боб", 200.0], "status": "missing" }
  ],
  "message": "Не хватает 1 строк."
}
```

---

## Структура проекта

```text
sql-trainer/
├── Makefile                        # Команды управления проектом
├── docker-compose.yml              # Полный стек (postgres, redis, backend)
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── pytest.ini                  # Настройка pytest (pythonpath, asyncio)
│   ├── .env.example
│   └── app/
│       ├── main.py                 # FastAPI app, CORS, lifespan, seed
│       ├── config.py               # Настройки (pydantic-settings + .env)
│       ├── api/
│       │   ├── deps.py             # get_current_user, require_teacher
│       │   └── routes/
│       │       ├── auth.py         # /register, /login
│       │       ├── tasks.py        # CRUD заданий
│       │       ├── execute.py      # /execute, /validate
│       │       ├── progress.py     # прогресс, лидерборд
│       │       └── teacher.py      # /sandbox (только teacher)
│       ├── core/
│       │   ├── sql_executor.py     # SQLite in-memory sandbox + таймаут
│       │   ├── result_comparator.py# ordered/unordered сравнение + diff
│       │   ├── query_validator.py  # whitelist SELECT, блокировка DDL/DML
│       │   ├── schema_parser.py    # DDL → список таблиц/колонок для UI
│       │   └── security.py         # JWT, bcrypt
│       ├── models/                 # SQLAlchemy: User, Task, Submission, Progress
│       ├── schemas/                # Pydantic: схемы запросов/ответов
│       ├── db/
│       │   ├── session.py          # AsyncSession, Base
│       │   └── seed/tasks.py       # 5 начальных заданий (SELECT → JOIN)
│       └── tests/
│           ├── test_executor.py    # 12 тестов
│           └── test_comparator.py  # 7 тестов
│
└── frontend/
    ├── vite.config.ts              # Vite + Tailwind + proxy /api → :8000
    └── src/
        ├── App.tsx                 # Роутинг, QueryClient, PrivateRoute
        ├── types/index.ts          # TypeScript типы
        ├── api/                    # Axios-клиент + функции по модулям
        ├── store/                  # Zustand: authStore, workspaceStore
        ├── components/
        │   ├── ui/                 # Button, Badge, Spinner
        │   ├── layout/             # Header
        │   ├── task/               # TaskDescription, SchemaViewer
        │   └── workspace/          # SqlEditor, ResultTable, ComparePanel
        └── pages/
            ├── LoginPage.tsx       # Вход + регистрация
            ├── TaskListPage.tsx    # Список заданий + прогресс
            ├── WorkspacePage.tsx   # Редактор + результаты
            └── teacher/
                ├── TeacherPage.tsx # Список заданий + удаление
                └── TaskFormPage.tsx# Форма создания задания
```

---

## Production деплой

Перед деплоем обязательно:

1. Установить надёжный `SECRET_KEY` в `.env`
2. Сменить пароль PostgreSQL
3. Настроить Nginx как reverse proxy
4. Включить HTTPS (Let's Encrypt / Certbot)
5. Убрать `DEBUG=true`

```bash
# Сгенерировать SECRET_KEY
openssl rand -hex 32
```
