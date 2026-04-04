from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import AsyncSessionLocal
from app.models.ai_recommendation_job import AIJobStatusEnum, AIRecommendationJob
from app.models.career_test_attempt import CareerTestAttempt
from app.models.test_methodology import TestMethodology
from app.repositories.career_test import CareerTestRepository
from app.services.bothub_ai import BothubAIClient
from app.services.hh import HeadHunterClient


async def process_ai_recommendation_job(job_id: str) -> None:
    async with AsyncSessionLocal() as db:
        repo = CareerTestRepository(db)
        ai = BothubAIClient()
        hh = HeadHunterClient()

        result = await db.execute(
            select(AIRecommendationJob)
            .where(AIRecommendationJob.id == job_id)
            .options(
                selectinload(AIRecommendationJob.attempt).selectinload(CareerTestAttempt.methodology),
                selectinload(AIRecommendationJob.attempt).selectinload(CareerTestAttempt.score),
                selectinload(AIRecommendationJob.attempt).selectinload(CareerTestAttempt.recommendation),
            )
        )
        job = result.scalar_one_or_none()
        if job is None:
            return

        try:
            job.status = AIJobStatusEnum.processing
            job.error_message = None
            await db.commit()
            await db.refresh(job)

            attempt = job.attempt
            if attempt is None or attempt.score is None:
                job.status = AIJobStatusEnum.failed
                job.error_message = 'Attempt or score not found'
                await db.commit()
                return

            methodology = attempt.methodology
            if methodology is None:
                methodology = await db.get(TestMethodology, attempt.methodology_id)
            if methodology is None:
                job.status = AIJobStatusEnum.failed
                job.error_message = 'Methodology not found'
                await db.commit()
                return

            if attempt.age_at_test is None or attempt.sex_snapshot is None or attempt.education_level_snapshot is None:
                job.status = AIJobStatusEnum.failed
                job.error_message = 'User profile is incomplete for AI processing'
                await db.commit()
                return

            ai_result = await ai.analyze_test_result(
                profile_snapshot={
                    'age': attempt.age_at_test,
                    'sex': attempt.sex_snapshot,
                    'education_level': attempt.education_level_snapshot,
                    'work_experience': attempt.work_experience_snapshot,
                    'hobbies_text': attempt.hobbies_text,
                },
                score_summary=attempt.score_summary_json,
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
                model_name='fallback' if not ai_result.get('model_name') else ai_result['model_name'],
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
            if job.attempt is not None:
                job.attempt.latest_error = str(exc)
            await db.commit()
