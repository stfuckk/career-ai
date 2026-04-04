from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.ai_recommendation_job import AIRecommendationJob
from app.models.career_recommendation import CareerRecommendation
from app.models.career_test_attempt import CareerTestAttempt
from app.models.career_test_score import CareerTestScore
from app.models.course_recommendation import CourseRecommendation
from app.models.test_methodology import TestMethodology
from app.models.vacancy_recommendation import VacancyRecommendation


class CareerTestRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_active_methodology(self, slug: str | None = None) -> TestMethodology | None:
        query = select(TestMethodology).where(TestMethodology.is_active.is_(True))
        if slug:
            query = query.where(TestMethodology.slug == slug)
        query = query.order_by(TestMethodology.created_at.desc())
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_attempt(self, **kwargs) -> CareerTestAttempt:
        attempt = CareerTestAttempt(**kwargs)
        self.db.add(attempt)
        await self.db.flush()
        await self.db.refresh(attempt)
        return attempt

    async def create_score(self, **kwargs) -> CareerTestScore:
        score = CareerTestScore(**kwargs)
        self.db.add(score)
        await self.db.flush()
        await self.db.refresh(score)
        return score

    async def upsert_recommendation(self, attempt: CareerTestAttempt, **kwargs) -> CareerRecommendation:
        result = await self.db.execute(
            select(CareerRecommendation).where(CareerRecommendation.attempt_id == attempt.id)
        )
        recommendation = result.scalar_one_or_none()
        if recommendation is None:
            recommendation = CareerRecommendation(attempt_id=attempt.id, **kwargs)
            self.db.add(recommendation)
        else:
            for key, value in kwargs.items():
                setattr(recommendation, key, value)
        await self.db.flush()
        await self.db.refresh(recommendation)
        return recommendation

    async def replace_vacancies(
        self,
        recommendation: CareerRecommendation,
        vacancies: list[dict],
    ) -> list[VacancyRecommendation]:
        result = await self.db.execute(
            select(VacancyRecommendation).where(VacancyRecommendation.recommendation_id == recommendation.id)
        )
        for entity in result.scalars().all():
            await self.db.delete(entity)
        await self.db.flush()
        entities = [
            VacancyRecommendation(
                recommendation_id=recommendation.id,
                hh_vacancy_id=item['hh_vacancy_id'],
                title=item['title'],
                employer_name=item.get('employer_name'),
                area_name=item.get('area_name'),
                alternate_url=item['alternate_url'],
                salary_from=item.get('salary_from'),
                salary_to=item.get('salary_to'),
                currency=item.get('currency'),
                snippet=item.get('snippet'),
            )
            for item in vacancies
        ]
        self.db.add_all(entities)
        await self.db.flush()
        return entities

    async def replace_courses(
        self,
        recommendation: CareerRecommendation,
        courses_by_step: dict[int, list[dict]],
    ) -> list[CourseRecommendation]:
        """Заменяет все курсы рекомендации на новые, привязанные к шагам career_path."""
        result = await self.db.execute(
            select(CourseRecommendation).where(CourseRecommendation.recommendation_id == recommendation.id)
        )
        for entity in result.scalars().all():
            await self.db.delete(entity)
        await self.db.flush()

        entities = []
        for step_index, courses in courses_by_step.items():
            for item in courses:
                entities.append(
                    CourseRecommendation(
                        recommendation_id=recommendation.id,
                        step_index=step_index,
                        skill=item['skill'],
                        stepik_course_id=item['stepik_course_id'],
                        title=item['title'],
                        summary=item.get('summary'),
                        url=item['url'],
                        cover_url=item.get('cover_url'),
                        price=item.get('price'),
                        currency=item.get('currency'),
                        is_free=item.get('is_free', True),
                        time_to_complete_hours=item.get('time_to_complete_hours'),
                        total_units=item.get('total_units'),
                        learners_count=item.get('learners_count', 0),
                        average_rating=item.get('average_rating'),
                    )
                )
        if entities:
            self.db.add_all(entities)
            await self.db.flush()
        return entities

    async def get_attempt_by_token(self, attempt_token: str) -> CareerTestAttempt | None:
        result = await self.db.execute(
            select(CareerTestAttempt)
            .where(CareerTestAttempt.public_token == attempt_token)
            .options(
                selectinload(CareerTestAttempt.score),
                selectinload(CareerTestAttempt.recommendation).selectinload(CareerRecommendation.vacancies),
                selectinload(CareerTestAttempt.recommendation).selectinload(CareerRecommendation.courses),
                selectinload(CareerTestAttempt.methodology),
                selectinload(CareerTestAttempt.ai_job),
            )
        )
        return result.scalar_one_or_none()

    async def get_latest_attempt_for_user(self, user_id: int) -> CareerTestAttempt | None:
        result = await self.db.execute(
            select(CareerTestAttempt)
            .where(CareerTestAttempt.user_id == user_id)
            .order_by(CareerTestAttempt.created_at.desc())
            .options(
                selectinload(CareerTestAttempt.score),
                selectinload(CareerTestAttempt.recommendation).selectinload(CareerRecommendation.vacancies),
                selectinload(CareerTestAttempt.recommendation).selectinload(CareerRecommendation.courses),
                selectinload(CareerTestAttempt.methodology),
                selectinload(CareerTestAttempt.ai_job),
            )
        )
        return result.scalars().first()
