from sqlalchemy import ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class CareerRecommendation(TimestampMixin, Base):
    __tablename__ = "career_recommendations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("survey_sessions.id", ondelete="CASCADE"), unique=True, index=True
    )
    summary: Mapped[str] = mapped_column(Text)
    suitable_roles: Mapped[list] = mapped_column(JSON)
    strengths: Mapped[list] = mapped_column(JSON)
    development_zones: Mapped[list] = mapped_column(JSON)
    next_steps: Mapped[list] = mapped_column(JSON)
    hh_vacancies: Mapped[list] = mapped_column(JSON, default=list)
    raw_ai_response: Mapped[dict] = mapped_column(JSON, default=dict)

    session = relationship("SurveySession", back_populates="recommendation")
