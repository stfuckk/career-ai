from enum import StrEnum
from uuid import uuid4

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class AIJobStatusEnum(StrEnum):
    pending = 'pending'
    processing = 'processing'
    ready = 'ready'
    failed = 'failed'


class AIRecommendationJob(TimestampMixin, Base):
    __tablename__ = 'ai_recommendation_jobs'

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    attempt_id: Mapped[int] = mapped_column(
        ForeignKey('career_test_attempts.id', ondelete='CASCADE'),
        unique=True,
        index=True,
    )
    status: Mapped[str] = mapped_column(String(32), default=AIJobStatusEnum.pending, index=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    attempt = relationship('CareerTestAttempt', back_populates='ai_job')
