from fastapi import APIRouter

from app.api.v1.endpoints.ai_jobs import router as ai_jobs_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.test_attempts import router as test_attempts_router
from app.api.v1.endpoints.test_methodologies import router as test_methodologies_router
from app.api.v1.endpoints.users import router as users_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(ai_jobs_router)
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(test_methodologies_router)
api_router.include_router(test_attempts_router)
