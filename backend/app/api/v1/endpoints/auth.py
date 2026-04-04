from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.auth import AuthResponse, UserLoginRequest, UserRegisterRequest
from app.schemas.user import UserRead
from app.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register_user(payload: UserRegisterRequest, db: AsyncSession = Depends(get_db_session)) -> AuthResponse:
    user, token = await AuthService(db).register(payload)
    return AuthResponse(access_token=token, user=UserRead.model_validate(user))


@router.post('/token', response_model=AuthResponse)
async def login_user(payload: UserLoginRequest, db: AsyncSession = Depends(get_db_session)) -> AuthResponse:
    user, token = await AuthService(db).login(payload)
    return AuthResponse(access_token=token, user=UserRead.model_validate(user))
