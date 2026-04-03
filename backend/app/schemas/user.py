from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import TimestampedRead


class UserRead(TimestampedRead):
    id: int
    email: EmailStr
    full_name: str | None
    is_active: bool


class UserUpdateRequest(BaseModel):
    full_name: str | None = Field(default=None, max_length=255)
