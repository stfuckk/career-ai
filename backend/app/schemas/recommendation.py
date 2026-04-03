from typing import Any

from pydantic import BaseModel, HttpUrl

from app.schemas.common import TimestampedRead


class VacancyRead(BaseModel):
    id: str
    name: str
    employer_name: str | None
    area_name: str | None
    salary_from: int | None = None
    salary_to: int | None = None
    currency: str | None = None
    alternate_url: HttpUrl | None = None
    snippet: dict[str, Any] | None = None
    published_at: str | None = None


class CareerRecommendationRead(TimestampedRead):
    id: int
    session_id: int
    summary: str
    suitable_roles: list[str]
    strengths: list[str]
    development_zones: list[str]
    next_steps: list[str]
    hh_vacancies: list[VacancyRead]
    raw_ai_response: dict[str, Any]
