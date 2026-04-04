import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    app_name: str
    api_v1_prefix: str
    debug: bool

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    database_url: str

    ai_base_url: str
    ai_api_key: str
    ai_model: str
    ai_timeout_seconds: int

    hh_base_url: str
    hh_api_token: str
    hh_user_agent: str
    hh_per_page: int


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv('APP_NAME', 'Career Guidance API'),
        api_v1_prefix=os.getenv('API_V1_PREFIX', '/api/v1'),
        debug=os.getenv('DEBUG', 'true').lower() == 'true',
        secret_key=os.getenv('SECRET_KEY', 'change-me'),
        algorithm=os.getenv('ALGORITHM', 'HS256'),
        access_token_expire_minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '120')),
        database_url=os.getenv(
            'DATABASE_URL',
            'postgresql+asyncpg://postgres:postgres@localhost:5432/career_guidance',
        ),
        ai_base_url=os.getenv('AI_BASE_URL', 'https://openai.bothub.chat/v1'),
        ai_api_key=os.getenv('AI_API_KEY', ''),
        ai_model=os.getenv('AI_MODEL', 'gpt-5.4-mini'),
        ai_timeout_seconds=int(os.getenv('AI_TIMEOUT_SECONDS', '45')),
        hh_base_url=os.getenv('HH_BASE_URL', 'https://api.hh.ru'),
        hh_api_token=os.getenv('HH_API_TOKEN', ''),
        hh_user_agent=os.getenv('HH_USER_AGENT', 'career-guidance-backend/0.1'),
        hh_per_page=int(os.getenv('HH_PER_PAGE', '10')),
    )


settings = get_settings()
