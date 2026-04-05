from app.models.ai_recommendation_job import AIJobStatusEnum, AIRecommendationJob
from app.models.career_recommendation import CareerRecommendation
from app.models.career_test_attempt import CareerTestAttempt
from app.models.career_test_score import CareerTestScore
from app.models.course_recommendation import CourseRecommendation
from app.models.test_methodology import TestMethodology
from app.models.user import User
from app.models.vacancy_recommendation import VacancyRecommendation

__all__ = [
    'AIJobStatusEnum',
    'AIRecommendationJob',
    'User',
    'TestMethodology',
    'CareerTestAttempt',
    'CareerTestScore',
    'CareerRecommendation',
    'CourseRecommendation',
    'VacancyRecommendation',
]
