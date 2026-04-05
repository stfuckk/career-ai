from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_login(self, login: str) -> User | None:
        result = await self.db.execute(select(User).where(User.login == login))
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        login: str,
        password_hash: str,
        sex: str,
        education_level: str,
        work_experience: int | None,
        hobbies_text: str | None = None,
        is_first_time_completing_test: bool,
    ) -> User:
        user = User(
            login=login,
            password_hash=password_hash,
            sex=sex,
            education_level=education_level,
            work_experience=work_experience,
            hobbies_text=hobbies_text,
            is_first_time_completing_test=is_first_time_completing_test,
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
