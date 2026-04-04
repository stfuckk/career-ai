from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class CareerRecommendation(TimestampMixin, Base):
    __tablename__ = 'career_recommendations'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    attempt_id: Mapped[int] = mapped_column(ForeignKey('career_test_attempts.id', ondelete='CASCADE'), unique=True)
    summary: Mapped[str] = mapped_column(Text)
    recommended_professions: Mapped[list] = mapped_column(JSON, default=list)
    hh_search_queries: Mapped[list[str]] = mapped_column(JSON, default=list)
    model_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    raw_ai_response: Mapped[dict] = mapped_column(JSON, default=dict)

    attempt = relationship('CareerTestAttempt', back_populates='recommendation')
    vacancies = relationship(
        'VacancyRecommendation',
        back_populates='recommendation',
        cascade='all, delete-orphan',
    )
