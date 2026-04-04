import asyncio
import logging
import sys
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import AsyncSessionLocal, engine
from app.models import *  # noqa: F403
from app.services.methodology import MethodologyService


def setup_logging() -> None:
    """Configure structured logging for the application."""
    log_level = logging.DEBUG if settings.debug else logging.INFO

    # Root logger — INFO or DEBUG depending on settings
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        stream=sys.stdout,
        force=True,
    )

    # SQLAlchemy engine/pool logs — always WARNING to avoid SQL spam
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)

    # httpx/httpcore — WARNING (avoid noisy HTTP debug logs)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)

    # uvicorn access logs — keep at INFO
    logging.getLogger('uvicorn.access').setLevel(logging.INFO)


setup_logging()
logger = logging.getLogger(__name__)


async def wait_for_database() -> None:
    last_error: Exception | None = None
    for attempt in range(1, settings.db_connect_max_retries + 1):
        try:
            async with engine.connect() as connection:
                await connection.execute(text('SELECT 1'))
            logger.info('Database connected')
            return
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt == settings.db_connect_max_retries:
                break
            logger.warning('Database connection attempt %d/%d failed: %s', attempt, settings.db_connect_max_retries, exc)
            await asyncio.sleep(settings.db_connect_retry_delay_seconds)
    if last_error is not None:
        raise last_error


@asynccontextmanager
async def lifespan(_: FastAPI):
    await wait_for_database()

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    logger.info('Database tables ensured')

    async with AsyncSessionLocal() as session:
        await MethodologyService(session).ensure_seeded()
    logger.info('Methodology seeded')

    yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
    docs_url='/docs',
    redoc_url='/redoc',
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch any unhandled exception, log it with full traceback, return 500."""
    logger.error(
        'Unhandled exception on %s %s: %s',
        request.method,
        request.url.path,
        exc,
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={'detail': f'Internal Server Error: {type(exc).__name__}: {exc}'},
    )


@app.middleware('http')
async def request_logging_middleware(request: Request, call_next):
    """Log every request with method, path, status, and duration."""
    start = time.monotonic()
    response = await call_next(request)
    elapsed_ms = (time.monotonic() - start) * 1000
    logger.info(
        '%s %s → %d (%.0fms)',
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response


app.include_router(api_router, prefix=settings.api_v1_prefix)
