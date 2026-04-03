import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = Field(default=os.getenv("APP_NAME", "Career Guidance API"))
    api_v1_prefix: str = Field(default=os.getenv("API_V1_PREFIX", "/api/v1"))
    debug: bool = Field(default=os.getenv("DEBUG", "true").lower() == "true")

    secret_key: str = Field(default=os.getenv("SECRET_KEY", "change-me"))
    algorithm: str = Field(default=os.getenv("ALGORITHM", "HS256"))
    access_token_expire_minutes: int = Field(
        default=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))
    )

    database_url: str = Field(
        default=os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://postgres:postgres@localhost:5432/career_guidance",
        )
    )

    ai_base_url: str = Field(
        default=os.getenv("AI_BASE_URL", "https://openai.bothub.chat/v1")
    )
    ai_api_key: str = Field(default=os.getenv("AI_API_KEY", ""))
    ai_model: str = Field(default=os.getenv("AI_MODEL", "gpt-5.4-mini"))
    ai_timeout_seconds: int = Field(
        default=int(os.getenv("AI_TIMEOUT_SECONDS", "45"))
    )

    hh_base_url: str = Field(default=os.getenv("HH_BASE_URL", "https://api.hh.ru"))
    hh_api_token: str = Field(default=os.getenv("HH_API_TOKEN", ""))
    hh_user_agent: str = Field(
        default=os.getenv("HH_USER_AGENT", "career-guidance-backend/0.1")
    )
    hh_per_page: int = Field(default=int(os.getenv("HH_PER_PAGE", "10")))

    frontend_url: str = Field(
        default=os.getenv("FRONTEND_URL", "http://localhost:5173")
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()