# Career Guidance Backend

Бэкенд сервиса профориентации для пользователей. Пользователь проходит тест, бэкенд сохраняет результат, запускает AI-анализ и возвращает персональные рекомендации с курсами (Stepik) и вакансиями (HH).

## Стек

- **Python 3.11+**
- **FastAPI** — async HTTP framework
- **SQLAlchemy 2.0** — async ORM (asyncpg)
- **PostgreSQL** — основная БД
- **Pydantic v2** — валидация данных
- **JWT + bcrypt** — аутентификация
- **httpx** — async HTTP-клиент (Bothub AI, HH API, Stepik API)
- **Uvicorn** — ASGI-сервер

## Быстрый старт

### 1. PostgreSQL через Docker

```bash
docker compose up -d
```

### 2. Зависимости

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -e ".[dev]"     # pytest, ruff
```

### 3. Переменные окружения

```bash
cp .env.example .env
```

Заполнить в `.env`:

```
AI_API_KEY=<ключ Bothub>
HH_API_TOKEN=<токен HH, опционально>
SECRET_KEY=<случайная строка 32+ символов>
```

Остальные переменные имеют рабочие дефолты для локальной разработки.

### 4. Запуск

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

При старте бэкенд сам:
- дожидается PostgreSQL
- создаёт таблицы
- сидирует методику теста

Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

## Структура проекта

```
app/
├── api/v1/endpoints/     # Роутеры FastAPI
├── core/                 # Config, JWT, bcrypt
├── db/                   # Engine, session, Base
├── models/               # SQLAlchemy-модели
├── repositories/         # Запросы к БД
├── schemas/              # Pydantic-схемы
├── services/             # Бизнес-логика
│   ├── ai_jobs.py        # BackgroundTask pipeline
│   ├── bothub_ai.py      # AI-клиент (OpenAI-compatible)
│   ├── hh.py             # HeadHunter API
│   ├── courses.py        # Stepik API
│   └── career_test.py    # Сериализация результатов
└── main.py               # FastAPI app + lifespan
```