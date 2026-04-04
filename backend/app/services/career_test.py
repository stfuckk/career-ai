from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.career_test_attempt import CareerTestAttempt
from app.repositories.career_test import CareerTestRepository
from app.schemas.career_test import CareerTestSubmitAnonymousRequest
from app.services.methodology import MethodologyService

CATEGORY_META = {
    'people': 'Работа с людьми',
    'research': 'Исследовательская деятельность',
    'practical': 'Практическая деятельность',
    'aesthetic': 'Эстетическая деятельность',
    'extreme': 'Экстремальная деятельность',
    'economic': 'Планово-экономическая деятельность',
}


def score_label(score: int) -> str:
    if 10 <= score <= 12:
        return 'ярко выраженная профессиональная склонность'
    if 7 <= score <= 9:
        return 'склонность к определенному виду деятельности'
    if 4 <= score <= 6:
        return 'слабо выраженная профессиональная склонность'
    return 'профессиональная склонность не выражена'


class CareerTestService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repo = CareerTestRepository(db)
        self.methodology_service = MethodologyService(db)

    async def get_methodology(self):
        return await self.methodology_service.get_active()

    async def create_attempt_and_score(self, payload: CareerTestSubmitAnonymousRequest) -> CareerTestAttempt:
        methodology = await self.get_methodology()

        attempt = await self.repo.create_attempt(
            methodology_id=methodology.id,
            status='completed',
            preview_summary='Тест пройден. Мы определили ваши ведущие профессиональные склонности и сохранили результат.',
        )

        score_summary = self._build_score_summary(payload)
        dominant_categories = self._extract_dominant_categories(score_summary)

        await self.repo.create_score(
            attempt_id=attempt.id,
            people_score=payload.scores.people_score,
            research_score=payload.scores.research_score,
            practical_score=payload.scores.practical_score,
            aesthetic_score=payload.scores.aesthetic_score,
            extreme_score=payload.scores.extreme_score,
            economic_score=payload.scores.economic_score,
            dominant_categories=dominant_categories,
            interpretation={item['key']: item for item in score_summary},
        )

        attempt.score_summary_json = score_summary
        await self.db.commit()

        # ВАЖНО: перечитываем attempt уже с eager-loaded relationship'ами
        loaded_attempt = await self.repo.get_attempt_by_token(attempt.public_token)
        if loaded_attempt is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Attempt was created but could not be reloaded',
            )
        return loaded_attempt

    async def get_attempt_preview(self, attempt_token: str):
        attempt = await self.repo.get_attempt_by_token(attempt_token)
        if attempt is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Attempt not found')
        return attempt

    async def get_latest_result_for_user(self, user_id: int):
        attempt = await self.repo.get_latest_attempt_for_user(user_id)
        if attempt is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Test result not found')
        if attempt.recommendation is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Result is not ready yet')
        return attempt

    def serialize_methodology(self, methodology) -> dict:
        parsed = methodology.parsed_json
        return {
            'id': methodology.id,
            'created_at': methodology.created_at,
            'updated_at': methodology.updated_at,
            'slug': methodology.slug,
            'version': methodology.version,
            'title': methodology.title,
            'source_pdf_name': methodology.source_pdf_name,
            'questions': parsed['questions'],
            'categories': parsed['categories'],
            'interpretation_ranges': [
                {
                    'from_score': item['from'],
                    'to_score': item['to'],
                    'label': item['label'],
                }
                for item in parsed['interpretation_ranges']
            ],
        }

    def serialize_preview(self, attempt: CareerTestAttempt) -> dict:
        return {
            'attempt_token': attempt.public_token,
            'methodology_slug': attempt.methodology.slug,
            'preview_summary': attempt.preview_summary or 'Результат сформирован.',
            'scores': attempt.score_summary_json,
            'dominant_categories': attempt.score.dominant_categories if attempt.score else [],
            'registration_required': True,
        }

    def serialize_result(self, attempt: CareerTestAttempt) -> dict:
        recommendation = attempt.recommendation
        return {
            'created_at': attempt.created_at.isoformat(),
            'updated_at': attempt.updated_at.isoformat(),
            'attempt_token': attempt.public_token,
            'methodology_slug': attempt.methodology.slug,
            'summary': recommendation.summary if recommendation else attempt.preview_summary or '',
            'scores': attempt.score_summary_json,
            'dominant_categories': attempt.score.dominant_categories if attempt.score else [],
            'professions': recommendation.recommended_professions if recommendation else [],
            'vacancies': [
                {
                    'hh_vacancy_id': item.hh_vacancy_id,
                    'title': item.title,
                    'employer_name': item.employer_name,
                    'area_name': item.area_name,
                    'alternate_url': item.alternate_url,
                    'salary_from': item.salary_from,
                    'salary_to': item.salary_to,
                    'currency': item.currency,
                    'snippet': item.snippet,
                }
                for item in (recommendation.vacancies if recommendation else [])
            ],
        }

    def _build_score_summary(self, payload: CareerTestSubmitAnonymousRequest) -> list[dict[str, Any]]:
        items = [
            ('people', payload.scores.people_score),
            ('research', payload.scores.research_score),
            ('practical', payload.scores.practical_score),
            ('aesthetic', payload.scores.aesthetic_score),
            ('extreme', payload.scores.extreme_score),
            ('economic', payload.scores.economic_score),
        ]
        return [
            {
                'key': key,
                'title': CATEGORY_META[key],
                'score': score,
                'label': score_label(score),
            }
            for key, score in items
        ]

    def _extract_dominant_categories(self, score_summary: list[dict]) -> list[str]:
        if not score_summary:
            return []
        max_score = max(item['score'] for item in score_summary)
        return [item['key'] for item in score_summary if item['score'] == max_score]


def serialize_score(score) -> dict[str, Any]:
    interpretation = score.interpretation or {}
    return {
        'people': interpretation.get('people'),
        'research': interpretation.get('research'),
        'practical': interpretation.get('practical'),
        'aesthetic': interpretation.get('aesthetic'),
        'extreme': interpretation.get('extreme'),
        'economic': interpretation.get('economic'),
        'dominant_categories': score.dominant_categories,
    }