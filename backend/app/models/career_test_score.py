from sqlalchemy import ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class CareerTestScore(TimestampMixin, Base):
    __tablename__ = 'career_test_scores'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    attempt_id: Mapped[int] = mapped_column(ForeignKey('career_test_attempts.id', ondelete='CASCADE'), unique=True)

    people_score: Mapped[int] = mapped_column(Integer, default=0)
    research_score: Mapped[int] = mapped_column(Integer, default=0)
    practical_score: Mapped[int] = mapped_column(Integer, default=0)
    aesthetic_score: Mapped[int] = mapped_column(Integer, default=0)
    extreme_score: Mapped[int] = mapped_column(Integer, default=0)
    economic_score: Mapped[int] = mapped_column(Integer, default=0)

    dominant_categories: Mapped[list[str]] = mapped_column(JSON, default=list)
    interpretation: Mapped[dict] = mapped_column(JSON, default=dict)

    attempt = relationship('CareerTestAttempt', back_populates='score')
