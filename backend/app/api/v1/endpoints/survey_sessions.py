from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.recommendation import CareerRecommendationRead
from app.schemas.survey import (
    SurveyAnswersSubmitRequest,
    SurveyAnswersSubmitResponse,
    SurveyQuestionRead,
    SurveySessionCreateRequest,
    SurveySessionRead,
)
from app.services.survey import SurveyService

router = APIRouter(prefix="/survey-sessions", tags=["survey-sessions"])


@router.get("", response_model=list[SurveySessionRead])
async def list_survey_sessions(
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> list[SurveySessionRead]:
    sessions = await SurveyService(db).list_sessions(user=current_user)
    return [SurveySessionRead.model_validate(session) for session in sessions]


@router.post("", response_model=SurveySessionRead, status_code=status.HTTP_201_CREATED)
async def create_survey_session(
    payload: SurveySessionCreateRequest,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> SurveySessionRead:
    session = await SurveyService(db).create_session(user=current_user, payload=payload)
    return SurveySessionRead.model_validate(session)


@router.get("/{session_id}", response_model=SurveySessionRead)
async def read_survey_session(
    session_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> SurveySessionRead:
    session = await SurveyService(db).get_session(user=current_user, session_id=session_id)
    return SurveySessionRead.model_validate(session)


@router.get("/{session_id}/questions", response_model=list[SurveyQuestionRead])
async def list_survey_questions(
    session_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> list[SurveyQuestionRead]:
    session = await SurveyService(db).get_session(user=current_user, session_id=session_id)
    ordered_questions = sorted(session.questions, key=lambda item: item.sort_order)
    return [SurveyQuestionRead.model_validate(question) for question in ordered_questions]


@router.post("/{session_id}/answers", response_model=SurveyAnswersSubmitResponse)
async def submit_survey_answers(
    session_id: int,
    payload: SurveyAnswersSubmitRequest,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> SurveyAnswersSubmitResponse:
    session = await SurveyService(db).submit_answers(
        user=current_user,
        session_id=session_id,
        payload=payload,
    )
    return SurveyAnswersSubmitResponse(
        session_id=session.id,
        status=session.status,
        submitted_answers=len(payload.answers),
        recommendations_ready=False,
    )


@router.get("/{session_id}/recommendation", response_model=CareerRecommendationRead)
async def get_session_recommendation(
    session_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> CareerRecommendationRead:
    recommendation = await SurveyService(db).get_or_generate_recommendation(
        user=current_user,
        session_id=session_id,
    )
    return CareerRecommendationRead.model_validate(recommendation)
