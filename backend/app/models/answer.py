from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class SurveyAnswer(TimestampMixin, Base):
    __tablename__ = "survey_answers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("survey_sessions.id", ondelete="CASCADE"), index=True
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey("survey_questions.id", ondelete="CASCADE"), index=True
    )
    question_code: Mapped[str] = mapped_column(String(100), index=True)
    value_json: Mapped[dict | list | str | int | float | bool | None] = mapped_column(JSON)

    session = relationship("SurveySession", back_populates="answers")
