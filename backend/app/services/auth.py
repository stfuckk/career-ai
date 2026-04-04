from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_password_hash, verify_password
from app.repositories.career_test import CareerTestRepository
from app.repositories.user import UserRepository
from app.schemas.auth import UserLoginRequest, UserRegisterRequest


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.users = UserRepository(db)
        self.tests = CareerTestRepository(db)

    async def register(self, payload: UserRegisterRequest):
        existing = await self.users.get_by_login(payload.login)
        if existing is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Login already registered')

        attempt = await self.tests.get_attempt_by_token(payload.attempt_token)
        if attempt is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Attempt not found')
        if attempt.user_id is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Attempt already linked to user')

        user = await self.users.create(
            login=payload.login,
            password_hash=get_password_hash(payload.password),
            sex=attempt.sex_snapshot,
            education_level=attempt.education_level_snapshot,
            work_experience=attempt.work_experience_snapshot,
            is_first_time_completing_test=False,
        )
        attempt.user_id = user.id
        attempt.status = 'linked_to_user'
        await self.db.commit()
        await self.db.refresh(user)
        return user, create_access_token(str(user.id))

    async def login(self, payload: UserLoginRequest):
        user = await self.users.get_by_login(payload.login)
        if user is None or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
        return user, create_access_token(str(user.id))
