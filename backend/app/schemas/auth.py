from pydantic import BaseModel, Field

from app.models.enums import EducationLevelEnum, SexEnum
from app.schemas.user import UserRead


class UserRegisterRequest(BaseModel):
    login: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    attempt_token: str = Field(min_length=1, max_length=128)
    age: int = Field(ge=16, le=22)
    sex: SexEnum
    education_level: EducationLevelEnum
    work_experience_months: int | None = Field(default=None, ge=0)
    hobbies_text: str | None = Field(default=None, max_length=2000)


class UserLoginRequest(BaseModel):
    login: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class AuthResponse(TokenResponse):
    user: UserRead
    job_id: str | None = None
    job_status: str | None = None
