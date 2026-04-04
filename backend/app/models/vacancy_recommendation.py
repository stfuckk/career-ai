from sqlalchemy import ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class VacancyRecommendation(TimestampMixin, Base):
    __tablename__ = 'vacancy_recommendations'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    recommendation_id: Mapped[int] = mapped_column(ForeignKey('career_recommendations.id', ondelete='CASCADE'))

    hh_vacancy_id: Mapped[str] = mapped_column(String(50), index=True)
    title: Mapped[str] = mapped_column(String(255))
    employer_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    area_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    alternate_url: Mapped[str] = mapped_column(Text)
    salary_from: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_to: Mapped[int | None] = mapped_column(Integer, nullable=True)
    currency: Mapped[str | None] = mapped_column(String(10), nullable=True)
    snippet: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    recommendation = relationship('CareerRecommendation', back_populates='vacancies')
