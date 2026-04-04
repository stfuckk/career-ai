from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.career_test import CareerTestRepository
from app.resources.yovayshi_rezapkina import METHODOLOGY_SLUG, PARSED_JSON, PARSED_TEXT
from app.models.test_methodology import TestMethodology


class MethodologyService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repo = CareerTestRepository(db)

    async def ensure_seeded(self) -> TestMethodology:
        methodology = await self.repo.get_active_methodology(METHODOLOGY_SLUG)
        if methodology is not None:
            return methodology

        methodology = TestMethodology(
            slug=PARSED_JSON['slug'],
            version=PARSED_JSON['version'],
            title=PARSED_JSON['title'],
            source_pdf_name=PARSED_JSON['source_pdf_name'],
            parsed_text=PARSED_TEXT,
            parsed_json=PARSED_JSON,
            is_active=True,
        )
        self.db.add(methodology)
        await self.db.commit()
        await self.db.refresh(methodology)
        return methodology

    async def get_active(self) -> TestMethodology:
        methodology = await self.repo.get_active_methodology(METHODOLOGY_SLUG)
        if methodology is None:
            methodology = await self.ensure_seeded()
        return methodology
