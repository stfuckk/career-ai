from pydantic import BaseModel

from app.models.ai_recommendation_job import AIJobStatusEnum


class AIJobCreatedRead(BaseModel):
    attempt_token: str
    job_id: str
    status: AIJobStatusEnum


class AIJobStatusRead(BaseModel):
    job_id: str
    status: AIJobStatusEnum
    error_message: str | None = None
