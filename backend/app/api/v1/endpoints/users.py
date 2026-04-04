from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.dependencies import get_current_user
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.career_test import CareerTestResultRead
from app.schemas.user import UserRead, UserUpdateRequest
from app.services.career_test import CareerTestService

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/me', response_model=UserRead)
async def read_me(current_user: User = Depends(get_current_user)) -> UserRead:
    return UserRead.model_validate(current_user)


@router.patch('/me', response_model=UserRead)
async def update_me(
    payload: UserUpdateRequest,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    existing = await UserRepository(db).get_by_login(payload.login)
    if existing is not None and existing.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Login already registered')
    current_user.login = payload.login
    await db.commit()
    await db.refresh(current_user)
    return UserRead.model_validate(current_user)


@router.get('/me/latest-test-result', response_model=CareerTestResultRead)
async def read_latest_test_result(
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> CareerTestResultRead:
    service = CareerTestService(db)
    attempt = await service.get_latest_result_for_user(current_user.id)
    if attempt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No test result found')
    return CareerTestResultRead.model_validate(service.serialize_result(attempt))
