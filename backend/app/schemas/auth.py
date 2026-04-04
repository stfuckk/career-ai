from pydantic import BaseModel, Field

from app.schemas.user import UserRead


class UserRegisterRequest(BaseModel):
    login: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    attempt_token: str = Field(min_length=1, max_length=128)


class UserLoginRequest(BaseModel):
    login: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class AuthResponse(TokenResponse):
    user: UserRead
