# Career AI

Демонстрация доступно в формате видео и презентации в корне репозитория или по ссылке ниже

**Ссылка на демонстрационные файлы:** https://disk.yandex.ru/d/mLgwtGmi-F-UZA

## О проекте

Сервис профориентации: пользователь проходит карьерный тест; бэкенд сохраняет результат, запускает AI-анализ и возвращает персональные рекомендации с курсами (Stepik) и вакансиями (HH). Веб-интерфейс — Vue 3 и Vite; API — FastAPI и PostgreSQL.

## Стек (бэкенд)

- **Python 3.11+**
- **FastAPI** — async HTTP framework
- **SQLAlchemy 2.0** — async ORM (asyncpg)
- **PostgreSQL** — основная БД
- **Pydantic v2** — валидация данных
- **JWT + bcrypt** — аутентификация
- **httpx** — async HTTP-клиент (Bothub AI, HH API, Stepik API)
- **Uvicorn** — ASGI-сервер

## Быстрый старт (бэкенд)

Команды ниже — из каталога `backend`.

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

## Frontend

Нужен **Node.js** версии **20.19+** или **22.12+** (см. `engines` в `frontend/package.json`).

```bash
cd frontend
npm install
```

**Разработка** — dev-сервер Vite (адрес и порт смотрите в выводе команды, обычно `http://localhost:5173`):

```bash
npm run dev
```

**Просмотр production-сборки** — сначала соберите проект, затем поднимите preview:

```bash
npm run build
npm run preview -- --host 0.0.0.0 --port 5173
```

**Ссылка на Figma:** https://www.figma.com/design/a0EbK8Ta32oxko69sUTniQ/hac?node-id=84-239&p=f
