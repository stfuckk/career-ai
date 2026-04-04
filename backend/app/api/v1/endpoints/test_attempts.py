from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.career_test import CareerTestPreviewRead, CareerTestSubmitAnonymousRequest
from app.services.career_test import CareerTestService

router = APIRouter(prefix='/test-attempts', tags=['test-attempts'])


@router.post('/submit-anonymous', response_model=CareerTestPreviewRead, status_code=status.HTTP_201_CREATED)
async def submit_anonymous_test(
    payload: CareerTestSubmitAnonymousRequest,
    db: AsyncSession = Depends(get_db_session),
) -> CareerTestPreviewRead:
    service = CareerTestService(db)
    attempt = await service.create_attempt_and_score(payload)
    return CareerTestPreviewRead.model_validate(service.serialize_preview(attempt))


@router.get('/{attempt_token}/preview', response_model=CareerTestPreviewRead)
async def read_attempt_preview(
    attempt_token: str,
    db: AsyncSession = Depends(get_db_session),
) -> CareerTestPreviewRead:
    service = CareerTestService(db)
    attempt = await service.get_attempt_preview(attempt_token)
    return CareerTestPreviewRead.model_validate(service.serialize_preview(attempt))
