from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class CourseRecommendation(TimestampMixin, Base):
    __tablename__ = 'course_recommendations'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    recommendation_id: Mapped[int] = mapped_column(ForeignKey('career_recommendations.id', ondelete='CASCADE'))
    step_index: Mapped[int] = mapped_column(Integer, comment='Index of the career_path step (0-based)')
    skill: Mapped[str] = mapped_column(String(255), comment='Skill from skills_to_learn that matched this course')

    stepik_course_id: Mapped[int] = mapped_column(Integer, index=True)
    title: Mapped[str] = mapped_column(String(500))
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    url: Mapped[str] = mapped_column(Text)
    cover_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    price: Mapped[float | None] = mapped_column(Float, nullable=True)
    currency: Mapped[str | None] = mapped_column(String(10), nullable=True)
    is_free: Mapped[bool] = mapped_column(Boolean, default=True)

    time_to_complete_hours: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_units: Mapped[int | None] = mapped_column(Integer, nullable=True, comment='Number of lessons')
    learners_count: Mapped[int] = mapped_column(Integer, default=0)
    average_rating: Mapped[float | None] = mapped_column(Float, nullable=True)

    recommendation = relationship('CareerRecommendation', back_populates='courses')
