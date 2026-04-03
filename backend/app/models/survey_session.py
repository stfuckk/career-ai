from sqlalchemy import Enum, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import SessionStatus


class SurveySession(TimestampMixin, Base):
    __tablename__ = "survey_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    status: Mapped[SessionStatus] = mapped_column(
        Enum(SessionStatus), default=SessionStatus.created, index=True
    )
    title: Mapped[str] = mapped_column(String(255), default="Career guidance session")
    profile_snapshot: Mapped[dict] = mapped_column(JSON)
    latest_error: Mapped[str | None] = mapped_column(Text, nullable=True)

    user = relationship("User", back_populates="sessions")
    questions = relationship("SurveyQuestion", back_populates="session", cascade="all, delete-orphan")
    answers = relationship("SurveyAnswer", back_populates="session", cascade="all, delete-orphan")
    recommendation = relationship(
        "CareerRecommendation",
        back_populates="session",
        cascade="all, delete-orphan",
        uselist=False,
    )
