from uuid import uuid4

from sqlalchemy import ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class CareerTestAttempt(TimestampMixin, Base):
    __tablename__ = 'career_test_attempts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    public_token: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        default=lambda: str(uuid4()),
    )
    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    methodology_id: Mapped[int] = mapped_column(ForeignKey('test_methodologies.id', ondelete='RESTRICT'))
    status: Mapped[str] = mapped_column(String(50), default='completed', index=True)

    age_at_test: Mapped[int] = mapped_column(Integer)
    sex_snapshot: Mapped[str] = mapped_column(String(50))
    education_level_snapshot: Mapped[str] = mapped_column(String(50))
    work_experience_snapshot: Mapped[int | None] = mapped_column(Integer, nullable=True)
    hobbies_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    score_summary_json: Mapped[list] = mapped_column(JSON, default=list)
    preview_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    latest_error: Mapped[str | None] = mapped_column(Text, nullable=True)

    user = relationship('User', back_populates='attempts')
    methodology = relationship('TestMethodology')
    score = relationship(
        'CareerTestScore',
        back_populates='attempt',
        cascade='all, delete-orphan',
        uselist=False,
    )
    recommendation = relationship(
        'CareerRecommendation',
        back_populates='attempt',
        cascade='all, delete-orphan',
        uselist=False,
    )
    ai_job = relationship(
        'AIRecommendationJob',
        back_populates='attempt',
        cascade='all, delete-orphan',
        uselist=False,
    )
