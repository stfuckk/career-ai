from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    sex: Mapped[str] = mapped_column(String(255))
    education_level: Mapped[str] = mapped_column(String(255))
    work_experience: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_first_time_completing_test: Mapped[bool] = mapped_column(Boolean, default=True)

    attempts = relationship(
        'CareerTestAttempt',
        back_populates='user',
        cascade='all, delete-orphan',
    )
