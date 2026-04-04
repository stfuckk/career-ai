from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.models.ai_recommendation_job import AIRecommendationJob
from app.models.career_test_attempt import CareerTestAttempt
from app.models.career_test_score import CareerTestScore
from app.models.test_methodology import TestMethodology
from app.schemas.ai_job import AIJobCreatedRead
from app.schemas.career_test import CareerTestSubmitAnonymousRequest
from app.services.ai_jobs import process_ai_recommendation_job
from app.services.career_test import (
    build_interpretation,
    extract_dominant_categories,
)

router = APIRouter(prefix="/test-attempts", tags=["test-attempts"])


@router.post("/submit-anonymous", response_model=AIJobCreatedRead, status_code=status.HTTP_202_ACCEPTED)
async def submit_anonymous_test(
    payload: CareerTestSubmitAnonymousRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_db_session),
):
    methodology_stmt = (
        select(TestMethodology)
        .where(TestMethodology.is_active.is_(True))
        .limit(1)
    )
    methodology = (await session.execute(methodology_stmt)).scalar_one_or_none()
    if methodology is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active methodology not found",
        )

    attempt = CareerTestAttempt(
        methodology_id=methodology.id,
        age_at_test=payload.age,
        sex_snapshot=payload.sex,
        education_level_snapshot=payload.education_level,
        work_experience_snapshot=payload.work_experience_months,
        hobbies_text=payload.hobbies_text,
    )
    session.add(attempt)
    await session.flush()

    interpretation = build_interpretation(
        people_score=payload.scores.people_score,
        research_score=payload.scores.research_score,
        practical_score=payload.scores.practical_score,
        aesthetic_score=payload.scores.aesthetic_score,
        extreme_score=payload.scores.extreme_score,
        economic_score=payload.scores.economic_score,
    )
    dominant_categories = extract_dominant_categories(interpretation)

    score = CareerTestScore(
        attempt_id=attempt.id,
        people_score=payload.scores.people_score,
        research_score=payload.scores.research_score,
        practical_score=payload.scores.practical_score,
        aesthetic_score=payload.scores.aesthetic_score,
        extreme_score=payload.scores.extreme_score,
        economic_score=payload.scores.economic_score,
        interpretation=interpretation,
        dominant_categories=dominant_categories,
    )
    session.add(score)
    await session.flush()

    job = AIRecommendationJob(attempt_id=attempt.id)
    session.add(job)

    await session.commit()

    background_tasks.add_task(process_ai_recommendation_job, job.id)

    return {
        "attempt_token": attempt.public_token,
        "job_id": job.id,
        "status": job.status,
    }