from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.career_test_attempt import CareerTestAttempt
from app.models.career_test_score import CareerTestScore
from app.models.test_methodology import TestMethodology
from app.repositories.career_test import CareerTestRepository

_SCORE_KEYS = (
    'people',
    'research',
    'practical',
    'aesthetic',
    'extreme',
    'economic',
)


CATEGORY_META = {
    "people": {
        "title": "Работа с людьми",
        "description": "Общение, обучение, воспитание, обслуживание, управление людьми.",
    },
    "research": {
        "title": "Исследовательская деятельность",
        "description": "Научная деятельность, аналитика, рациональность, независимость суждений.",
    },
    "practical": {
        "title": "Практическая деятельность",
        "description": "Производство, монтаж, ремонт, наладка, работа с техникой и изделиями.",
    },
    "aesthetic": {
        "title": "Эстетическая деятельность",
        "description": "Творческие профессии: музыка, искусство, литература, сцена.",
    },
    "extreme": {
        "title": "Экстремальная деятельность",
        "description": "Спорт, экспедиции, служба, работа в необычных или сложных условиях.",
    },
    "economic": {
        "title": "Планово-экономическая деятельность",
        "description": "Расчеты, планирование, документооборот, анализ текстов, схемы.",
    },
}


def score_label(score: int) -> str:
    if 10 <= score <= 12:
        return "ярко выраженная склонность"
    if 7 <= score <= 9:
        return "склонность выражена"
    if 4 <= score <= 6:
        return "слабо выраженная склонность"
    return "склонность не выражена"


def build_interpretation(
    *,
    people_score: int,
    research_score: int,
    practical_score: int,
    aesthetic_score: int,
    extreme_score: int,
    economic_score: int,
) -> dict[str, Any]:
    return {
        "people": {
            "score": people_score,
            "label": score_label(people_score),
            "title": CATEGORY_META["people"]["title"],
        },
        "research": {
            "score": research_score,
            "label": score_label(research_score),
            "title": CATEGORY_META["research"]["title"],
        },
        "practical": {
            "score": practical_score,
            "label": score_label(practical_score),
            "title": CATEGORY_META["practical"]["title"],
        },
        "aesthetic": {
            "score": aesthetic_score,
            "label": score_label(aesthetic_score),
            "title": CATEGORY_META["aesthetic"]["title"],
        },
        "extreme": {
            "score": extreme_score,
            "label": score_label(extreme_score),
            "title": CATEGORY_META["extreme"]["title"],
        },
        "economic": {
            "score": economic_score,
            "label": score_label(economic_score),
            "title": CATEGORY_META["economic"]["title"],
        },
    }


def extract_dominant_categories(interpretation: dict[str, Any]) -> list[str]:
    max_score = max(item["score"] for item in interpretation.values())
    return [
        key
        for key, item in interpretation.items()
        if item["score"] == max_score
    ]


def serialize_score(score: CareerTestScore) -> dict[str, Any]:
    interpretation = score.interpretation
    return {
        "people": interpretation["people"],
        "research": interpretation["research"],
        "practical": interpretation["practical"],
        "aesthetic": interpretation["aesthetic"],
        "extreme": interpretation["extreme"],
        "economic": interpretation["economic"],
        "dominant_categories": score.dominant_categories,
    }


def interpretation_to_category_reads(interpretation: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key in _SCORE_KEYS:
        item = interpretation.get(key)
        if not item:
            continue
        rows.append(
            {
                'key': key,
                'title': item.get('title', ''),
                'score': item['score'],
                'label': item.get('label', ''),
            }
        )
    return rows


class CareerTestService:
    def __init__(self, db: AsyncSession) -> None:
        self._repo = CareerTestRepository(db)

    async def get_methodology(self) -> TestMethodology | None:
        return await self._repo.get_active_methodology()

    def serialize_methodology(self, methodology: TestMethodology) -> dict[str, Any]:
        data = methodology.parsed_json or {}
        ranges: list[dict[str, Any]] = []
        for r in data.get('interpretation_ranges', []):
            ranges.append(
                {
                    'from_score': r.get('from_score', r.get('from')),
                    'to_score': r.get('to_score', r.get('to')),
                    'label': r['label'],
                }
            )
        return {
            'slug': methodology.slug,
            'version': methodology.version,
            'title': methodology.title,
            'source_pdf_name': methodology.source_pdf_name,
            'questions': data.get('questions', []),
            'categories': data.get('categories', []),
            'interpretation_ranges': ranges,
        }

    async def get_latest_result_for_user(self, user_id: int) -> CareerTestAttempt | None:
        return await self._repo.get_latest_attempt_for_user(user_id)

    def serialize_preview(self, attempt: CareerTestAttempt) -> dict[str, Any]:
        score = attempt.score
        interpretation = score.interpretation if score else {}
        methodology = attempt.methodology
        return {
            'attempt_token': attempt.public_token,
            'methodology_slug': methodology.slug if methodology else '',
            'preview_summary': attempt.preview_summary or '',
            'scores': interpretation_to_category_reads(interpretation),
            'dominant_categories': list(score.dominant_categories) if score else [],
            'registration_required': True,
        }

    def serialize_result(self, attempt: CareerTestAttempt) -> dict[str, Any]:
        rec = attempt.recommendation
        score = attempt.score
        interpretation = score.interpretation if score else {}
        methodology = attempt.methodology
        professions: list[dict[str, Any]] = []
        if rec and rec.recommended_professions:
            for p in rec.recommended_professions:
                if isinstance(p, dict):
                    professions.append(
                        {
                            'name': p.get('name', ''),
                            'rationale': p.get('rationale', ''),
                            'fit_score': int(p.get('fit_score', 0)),
                        }
                    )
        vacancies: list[dict[str, Any]] = []
        if rec and rec.vacancies:
            for v in rec.vacancies:
                vacancies.append(
                    {
                        'hh_vacancy_id': v.hh_vacancy_id,
                        'title': v.title,
                        'employer_name': v.employer_name,
                        'area_name': v.area_name,
                        'alternate_url': v.alternate_url,
                        'salary_from': v.salary_from,
                        'salary_to': v.salary_to,
                        'currency': v.currency,
                        'snippet': v.snippet,
                    }
                )
        return {
            'created_at': attempt.created_at,
            'updated_at': attempt.updated_at,
            'attempt_token': attempt.public_token,
            'methodology_slug': methodology.slug if methodology else '',
            'summary': rec.summary if rec else '',
            'scores': interpretation_to_category_reads(interpretation),
            'dominant_categories': list(score.dominant_categories) if score else [],
            'professions': professions,
            'vacancies': vacancies,
        }


def build_llm_payload(*, methodology, attempt, score: CareerTestScore) -> dict[str, Any]:
    return {
        "test_name": methodology.title,
        "methodology_text": methodology.parsed_text,
        "methodology_meta": methodology.parsed_json,
        "user_profile": {
            "age": attempt.age_at_test,
            "sex": attempt.sex_snapshot.value if hasattr(attempt.sex_snapshot, "value") else attempt.sex_snapshot,
            "education_level": (
                attempt.education_level_snapshot.value
                if hasattr(attempt.education_level_snapshot, "value")
                else attempt.education_level_snapshot
            ),
            "work_experience": attempt.work_experience,
            "hobbies_text": attempt.hobbies_text,
        },
        "scores": {
            "people_score": score.people_score,
            "research_score": score.research_score,
            "practical_score": score.practical_score,
            "aesthetic_score": score.aesthetic_score,
            "extreme_score": score.extreme_score,
            "economic_score": score.economic_score,
        },
        "interpretation": score.interpretation,
    }