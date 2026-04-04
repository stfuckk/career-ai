from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import AsyncSessionLocal
from app.models.ai_recommendation_job import AIJobStatusEnum, AIRecommendationJob
from app.models.career_test_attempt import CareerTestAttempt
from app.models.career_recommendation import CareerRecommendation
from app.models.test_methodology import TestMethodology
from app.repositories.career_test import CareerTestRepository
from app.services.bothub_ai import BothubAIClient
from app.services.hh import HeadHunterClient


def _build_attempt_options():
    """Единый набор eager-load опций для attempt и его связей."""
    return [
        selectinload(AIRecommendationJob.attempt).selectinload(CareerTestAttempt.methodology),
        selectinload(AIRecommendationJob.attempt).selectinload(CareerTestAttempt.score),
        selectinload(AIRecommendationJob.attempt)
        .selectinload(CareerTestAttempt.recommendation)
        .selectinload(CareerRecommendation.vacancies),
    ]


async def _fetch_job(db, job_id: str) -> AIRecommendationJob | None:
    """Загружает job со всеми нужными связями. Использовать вместо db.refresh(job)."""
    result = await db.execute(
        select(AIRecommendationJob)
        .where(AIRecommendationJob.id == job_id)
        .options(*_build_attempt_options())
    )
    return result.scalar_one_or_none()


async def process_ai_recommendation_job(job_id: str) -> None:
    async with AsyncSessionLocal() as db:
        repo = CareerTestRepository(db)
        ai = BothubAIClient()
        hh = HeadHunterClient()

        job = await _fetch_job(db, job_id)
        if job is None:
            return

        try:
            # Помечаем как processing.
            # ВАЖНО: после commit не делаем db.refresh(job) — это сбросит relationships.
            # Вместо этого перечитываем job через _fetch_job.
            job.status = AIJobStatusEnum.processing
            job.error_message = None
            await db.commit()

            job = await _fetch_job(db, job_id)
            if job is None:
                return

            attempt = job.attempt
            if attempt is None:
                raise ValueError('Attempt not found for job')
            if attempt.score is None:
                raise ValueError('Score not found for attempt')

            methodology = attempt.methodology
            if methodology is None:
                methodology = await db.get(TestMethodology, attempt.methodology_id)
            if methodology is None:
                raise ValueError('Methodology not found')

            if attempt.age_at_test is None or attempt.sex_snapshot is None or attempt.education_level_snapshot is None:
                raise ValueError(
                    'User profile is incomplete (age/sex/education missing). '
                    'AI processing requires registration data.'
                )

            ai_result = await ai.analyze_test_result(
                profile_snapshot={
                    'age': attempt.age_at_test,
                    'sex': attempt.sex_snapshot,
                    'education_level': attempt.education_level_snapshot,
                    'work_experience_months': attempt.work_experience_snapshot,
                    'hobbies_text': attempt.hobbies_text,
                },
                score_summary=attempt.score_summary_json,
                dominant_categories=attempt.score.dominant_categories,
                methodology_text=methodology.parsed_text,
                methodology_json=methodology.parsed_json,
            )

            attempt.preview_summary = ai_result['preview_summary']
            attempt.latest_error = None

            recommendation = await repo.upsert_recommendation(
                attempt,
                summary=ai_result['summary'],
                recommended_professions=ai_result['recommended_professions'],
                hh_search_queries=ai_result['hh_search_queries'],
                model_name=ai_result.get('model_name'),
                prompt_version='v1',
                raw_ai_response=ai_result,
            )

            vacancies = await hh.search_vacancies(queries=recommendation.hh_search_queries)
            if vacancies:
                await repo.replace_vacancies(recommendation, vacancies)

            job.status = AIJobStatusEnum.ready
            job.error_message = None
            await db.commit()

        except Exception as exc:  # noqa: BLE001
            job.status = AIJobStatusEnum.failed
            job.error_message = str(exc)
            try:
                if job.attempt is not None:
                    job.attempt.latest_error = str(exc)
            except Exception:  # noqa: BLE001
                pass
            await db.commit()
