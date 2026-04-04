from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session

router = APIRouter(tags=['health'])


@router.get('/health')
async def healthcheck() -> dict[str, str]:
    return {'status': 'ok'}


@router.get('/health/db')
async def database_healthcheck(db: AsyncSession = Depends(get_db_session)) -> dict[str, str]:
    await db.execute(text('SELECT 1'))
    return {'status': 'ok'}
