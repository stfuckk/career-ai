from sqlalchemy import Boolean, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class TestMethodology(TimestampMixin, Base):
    __tablename__ = 'test_methodologies'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    version: Mapped[str] = mapped_column(String(50))
    title: Mapped[str] = mapped_column(String(255))
    source_pdf_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    parsed_text: Mapped[str] = mapped_column(Text)
    parsed_json: Mapped[dict] = mapped_column(JSON)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
