from sqlalchemy.ext.asyncio import AsyncSession

from app.models.test_methodology import TestMethodology
from app.repositories.career_test import CareerTestRepository
from app.resources.yovayshi_rezapkina import METHODOLOGY_SLUG, PARSED_JSON, PARSED_TEXT


class MethodologyService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repo = CareerTestRepository(db)

    async def ensure_seeded(self) -> None:
        existing = await self.repo.get_active_methodology(METHODOLOGY_SLUG)
        if existing is not None:
            return

        methodology = TestMethodology(
            slug=METHODOLOGY_SLUG,
            version='1.0',
            title='Определение профессиональных склонностей',
            source_pdf_name='Oprosnik-Yovashi-v-modif.-Rezapkinoy-_1_.pdf',
            parsed_text=PARSED_TEXT,
            parsed_json=PARSED_JSON,
            is_active=True,
        )
        self.db.add(methodology)
        await self.db.commit()

    async def get_active(self) -> TestMethodology:
        methodology = await self.repo.get_active_methodology(METHODOLOGY_SLUG)
        if methodology is None:
            await self.ensure_seeded()
            methodology = await self.repo.get_active_methodology(METHODOLOGY_SLUG)
        if methodology is None:
            raise RuntimeError('Active methodology not found')
        return methodology
