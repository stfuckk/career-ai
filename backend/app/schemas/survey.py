from typing import Any

from pydantic import BaseModel, Field, conint

from app.models.enums import EducationLevel, QuestionInputType, QuestionStage, SessionStatus
from app.schemas.common import TimestampedRead


class OnboardingPayload(BaseModel):
    age: conint(ge=16, le=22)
    education_level: EducationLevel
    education_details: str | None = Field(default=None, max_length=255)
    city: str | None = Field(default=None, max_length=120)
    interests: list[str] = Field(min_length=1, max_length=10)
    favorite_subjects: list[str] = Field(default_factory=list, max_length=10)
    preferred_work_format: str | None = Field(default=None, max_length=100)
    about_me: str | None = Field(default=None, max_length=1000)


class SurveySessionCreateRequest(BaseModel):
    title: str | None = Field(default="Career guidance session", max_length=255)
    onboarding: OnboardingPayload


class SurveySessionRead(TimestampedRead):
    id: int
    user_id: int
    title: str
    status: SessionStatus
    profile_snapshot: dict[str, Any]
    latest_error: str | None


class SurveyQuestionRead(TimestampedRead):
    id: int
    stage: QuestionStage
    code: str
    title: str
    description: str | None
    input_type: QuestionInputType
    options: list[dict[str, Any]] | list[str] | None
    sort_order: int
    metadata_json: dict[str, Any] | None


class SurveyAnswerInput(BaseModel):
    question_id: int
    question_code: str
    value: Any


class SurveyAnswersSubmitRequest(BaseModel):
    answers: list[SurveyAnswerInput] = Field(min_length=1)


class SurveyAnswersSubmitResponse(BaseModel):
    session_id: int
    status: SessionStatus
    submitted_answers: int
    recommendations_ready: bool
