import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.session import get_db_session
from app.models.ai_recommendation_job import AIJobStatusEnum, AIRecommendationJob
from app.models.career_recommendation import CareerRecommendation
from app.models.career_test_attempt import CareerTestAttempt
from app.models.course_recommendation import CourseRecommendation  # noqa: F401 — triggers mapper registration
from app.schemas.ai_job import AIJobStatusRead
from app.schemas.career_test import CareerTestResultRead
from app.services.career_test import CareerTestService

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/ai-jobs', tags=['ai-jobs'])


@router.get('/{job_id}/status', response_model=AIJobStatusRead)
async def get_ai_job_status(job_id: str, db: AsyncSession = Depends(get_db_session)) -> AIJobStatusRead:
    result = await db.execute(select(AIRecommendationJob).where(AIRecommendationJob.id == job_id))
    job = result.scalar_one_or_none()
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Job not found')
    return AIJobStatusRead(job_id=job.id, status=job.status, error_message=job.error_message)


@router.get('/{job_id}/result', response_model=CareerTestResultRead)
async def get_ai_job_result(job_id: str, db: AsyncSession = Depends(get_db_session)) -> CareerTestResultRead:
    result = await db.execute(
        select(AIRecommendationJob)
        .where(AIRecommendationJob.id == job_id)
        .options(
            selectinload(AIRecommendationJob.attempt).selectinload(CareerTestAttempt.score),
            selectinload(AIRecommendationJob.attempt).selectinload(CareerTestAttempt.methodology),
            selectinload(AIRecommendationJob.attempt)
            .selectinload(CareerTestAttempt.recommendation)
            .selectinload(CareerRecommendation.vacancies),
            selectinload(AIRecommendationJob.attempt)
            .selectinload(CareerTestAttempt.recommendation)
            .selectinload(CareerRecommendation.courses),
        )
    )
    job = result.scalar_one_or_none()
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Job not found')
    if job.status == AIJobStatusEnum.failed:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=job.error_message or 'Job failed',
        )
    if job.status != AIJobStatusEnum.ready:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Result is not ready yet')

    attempt = job.attempt
    if attempt is None or attempt.recommendation is None:
        logger.error('Job %s marked ready but attempt or recommendation is None', job_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Job marked ready but result not found',
        )

    service = CareerTestService(db)

    try:
        serialized = service.serialize_result(attempt)
    except (ValueError, KeyError, TypeError) as exc:
        logger.error(
            'serialize_result failed for job %s: %s',
            job_id,
            exc,
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Failed to serialize result: {exc}',
        ) from exc

    try:
        return CareerTestResultRead.model_validate(serialized)
    except ValidationError as exc:
        logger.error(
            'Pydantic validation failed for job %s: %s\nSerialized data keys: %s',
            job_id,
            exc,
            list(serialized.keys()) if isinstance(serialized, dict) else type(serialized).__name__,
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Result validation error: {exc.error_count()} validation error(s). '
            f'First: {exc.errors()[0]["msg"]} at {exc.errors()[0]["loc"]}',
        ) from exc
