from pydantic import BaseModel, Field

from app.schemas.common import TimestampedRead


class UserRead(TimestampedRead):
    id: int
    login: str
    is_active: bool
    sex: str
    education_level: str
    work_experience: int | None
    hobbies_text: str | None = None
    is_first_time_completing_test: bool


class UserUpdateRequest(BaseModel):
    login: str = Field(min_length=3, max_length=255)
