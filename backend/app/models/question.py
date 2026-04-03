from sqlalchemy import Enum, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import QuestionInputType, QuestionStage


class SurveyQuestion(TimestampMixin, Base):
    __tablename__ = "survey_questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("survey_sessions.id", ondelete="CASCADE"), index=True
    )
    stage: Mapped[QuestionStage] = mapped_column(Enum(QuestionStage), index=True)
    code: Mapped[str] = mapped_column(String(100), index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    input_type: Mapped[QuestionInputType] = mapped_column(Enum(QuestionInputType))
    options: Mapped[list | None] = mapped_column(JSON, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    session = relationship("SurveySession", back_populates="questions")
