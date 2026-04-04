from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.methodology import TestMethodologyRead
from app.services.career_test import CareerTestService

router = APIRouter(prefix='/test-methodologies', tags=['test-methodologies'])


@router.get('/current', response_model=TestMethodologyRead)
async def get_current_methodology(db: AsyncSession = Depends(get_db_session)) -> TestMethodologyRead:
    service = CareerTestService(db)
    methodology = await service.get_methodology()
    return TestMethodologyRead.model_validate(service.serialize_methodology(methodology))
