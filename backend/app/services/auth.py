from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.ai_recommendation_job import AIRecommendationJob
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
        if attempt.ai_job is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='AI job already exists for this attempt')

        user = await self.users.create(
            login=payload.login,
            password_hash=get_password_hash(payload.password),
            sex=payload.sex.value,
            education_level=payload.education_level.value,
            work_experience=payload.work_experience_months,
            is_first_time_completing_test=False,
        )

        attempt.user_id = user.id
        attempt.age_at_test = payload.age
        attempt.sex_snapshot = payload.sex.value
        attempt.education_level_snapshot = payload.education_level.value
        attempt.work_experience_snapshot = payload.work_experience_months
        attempt.hobbies_text = payload.hobbies_text
        attempt.status = 'linked_to_user'

        job = AIRecommendationJob(attempt_id=attempt.id)
        self.db.add(job)

        await self.db.commit()
        await self.db.refresh(user)
        await self.db.refresh(job)

        return user, create_access_token(str(user.id)), job

    async def login(self, payload: UserLoginRequest):
        user = await self.users.get_by_login(payload.login)
        if user is None or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
        return user, create_access_token(str(user.id))