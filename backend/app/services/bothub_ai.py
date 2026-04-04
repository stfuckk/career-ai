import json
import re
from typing import Any

import httpx

from app.core.config import get_settings

SYSTEM_PROMPT = """Ты карьерный консультант и помощник по профориентации для пользователей 16–22 лет.

Тебе будут переданы:
1. Профиль пользователя (возраст, пол, образование, опыт, интересы).
2. Уже рассчитанные результаты теста по 6 шкалам (key, title, score).
3. Ведущие категории (dominant_categories).
4. Методический текст и структура методики.

Твоя задача — вернуть JSON строго по указанной схеме для frontend UI.

Правила:
- НЕ пересчитывай score и НЕ меняй числовые значения.
- Используй только переданные key, title и score — не придумывай новые.
- Для каждого score в массиве scores верни только поле label (короткое, естественное пояснение для пользователя, 1–2 предложения).
- preview_summary — 1–2 предложения, краткий итог по профилю.
- best_specialty — одна наиболее подходящая специальность для этого пользователя.
- about_user — заполни на основе переданных данных профиля; не выдумывай факты, которых нет во входных данных.
- career_fit.professions — от 3 до 5 профессий, подходящих для начинающих или стажёров.
- development_recommendations.steps — ровно 3 конкретных, прикладных шага развития.
- hh_search_queries — 2–4 поисковых запроса для hh.ru, без лишних слов.
- Не добавляй markdown, не оборачивай в блоки кода, не добавляй текст вне JSON.
- Если данных недостаточно — всё равно верни корректный JSON, но не выдумывай факты."""


class BothubAIClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def analyze_test_result(
        self,
        *,
        profile_snapshot: dict[str, Any],
        score_summary: list[dict[str, Any]],
        dominant_categories: list[str],
        methodology_text: str,
        methodology_json: dict[str, Any],
    ) -> dict[str, Any]:
        if not self.settings.ai_api_key:
            raise RuntimeError('AI_API_KEY is not set')

        user_message = self._build_user_message(
            profile_snapshot=profile_snapshot,
            score_summary=score_summary,
            dominant_categories=dominant_categories,
            methodology_text=methodology_text,
            methodology_json=methodology_json,
        )

        response = await self._chat_json(user_message)
        return self._normalize_response(response, score_summary)

    def _build_user_message(
        self,
        *,
        profile_snapshot: dict[str, Any],
        score_summary: list[dict[str, Any]],
        dominant_categories: list[str],
        methodology_text: str,
        methodology_json: dict[str, Any],
    ) -> str:
        schema = {
            'preview_summary': 'string (1–2 предложения)',
            'best_specialty': 'string (одна специальность)',
            'summary': 'string (краткий итог для блока рекомендаций)',
            'scores': [
                {
                    'key': 'string (не менять)',
                    'label': 'string (пояснение для пользователя)',
                }
            ],
            'about_user': {
                'age': 'string',
                'experience': 'string',
                'strengths': ['string'],
                'education': 'string',
            },
            'career_fit': {
                'title': 'string',
                'summary': 'string',
                'professions': ['string (3–5 профессий)'],
            },
            'development_recommendations': {
                'title': 'string',
                'summary': 'string',
                'steps': ['string (ровно 3 шага)'],
            },
            'recommended_professions': [
                {
                    'name': 'string',
                    'rationale': 'string',
                    'fit_score': 'integer 0–100',
                }
            ],
            'hh_search_queries': ['string (2–4 запроса для hh.ru)'],
        }

        parts = [
            f'Схема ответа (верни строго этот JSON, без markdown):\n{json.dumps(schema, ensure_ascii=False, indent=2)}',
            f'\nПрофиль пользователя:\n{json.dumps(profile_snapshot, ensure_ascii=False, indent=2)}',
            f'\nРассчитанные результаты теста (key/title/score НЕ менять):\n{json.dumps(score_summary, ensure_ascii=False, indent=2)}',
            f'\nВедущие категории: {json.dumps(dominant_categories, ensure_ascii=False)}',
            f'\nМетодический текст:\n{methodology_text}',
            f'\nСтруктура методики:\n{json.dumps(methodology_json, ensure_ascii=False)}',
        ]

        return '\n'.join(parts)

    async def _chat_json(self, user_message: str) -> dict[str, Any]:
        payload = {
            'model': self.settings.ai_model,
            'messages': [
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': user_message},
            ],
            'temperature': 0.3,
        }
        headers = {
            'Authorization': f'Bearer {self.settings.ai_api_key}',
            'Content-Type': 'application/json',
        }

        async with httpx.AsyncClient(timeout=self.settings.ai_timeout_seconds) as client:
            response = await client.post(
                f"{self.settings.ai_base_url.rstrip('/')}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        content = data['choices'][0]['message']['content']
        if isinstance(content, list):
            content = ''.join(part.get('text', '') for part in content if isinstance(part, dict))
        return self._extract_json_object(content)

    def _extract_json_object(self, raw_text: str) -> dict[str, Any]:
        raw_text = raw_text.strip()
        if raw_text.startswith('```'):
            raw_text = re.sub(r'^```(?:json)?', '', raw_text).strip()
            raw_text = re.sub(r'```$', '', raw_text).strip()
        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError:
            match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if not match:
                raise ValueError('AI response does not contain a valid JSON object')
            parsed = json.loads(match.group(0))
        if not isinstance(parsed, dict):
            raise ValueError('Parsed AI response is not a JSON object')
        return parsed

    def _normalize_response(
        self,
        response: dict[str, Any],
        score_summary: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Строгая валидация ответа AI.
        Любое несоответствие поднимает ValueError → job переходит в failed.
        Никаких fallback-значений.
        """
        preview_summary = self._require_non_empty_string(response.get('preview_summary'), 'preview_summary')
        best_specialty = self._require_non_empty_string(response.get('best_specialty'), 'best_specialty')
        scores = self._merge_score_labels(score_summary, response.get('scores'))
        about_user = self._normalize_about_user(response.get('about_user'))
        career_fit = self._normalize_career_fit(response.get('career_fit'))
        development = self._normalize_development_recommendations(response.get('development_recommendations'))
        professions = self._ensure_profession_list(response.get('recommended_professions'))
        queries = self._ensure_string_list(response.get('hh_search_queries'), field_name='hh_search_queries', min_items=1)

        summary_value = response.get('summary')
        summary = summary_value.strip() if isinstance(summary_value, str) and summary_value.strip() else career_fit['summary']

        return {
            'preview_summary': preview_summary,
            'best_specialty': best_specialty,
            'scores': scores,
            'about_user': about_user,
            'career_fit': career_fit,
            'development_recommendations': development,
            'recommended_professions': professions,
            'hh_search_queries': queries,
            'summary': summary,
            'model_name': self.settings.ai_model,
        }

    def _merge_score_labels(self, baseline_scores: list[dict[str, Any]], value: Any) -> list[dict[str, Any]]:
        if not isinstance(value, list):
            raise ValueError('scores must be a list')

        labels_by_key: dict[str, str] = {}
        for item in value:
            if not isinstance(item, dict):
                continue
            key = str(item.get('key', '')).strip()
            label = str(item.get('label', '')).strip()
            if key and label:
                labels_by_key[key] = label

        missing_keys = [item['key'] for item in baseline_scores if item['key'] not in labels_by_key]
        if missing_keys:
            raise ValueError(f"AI response is missing labels for keys: {', '.join(missing_keys)}")

        # Берём key/title/score из backend-истины, label — из AI
        return [
            {
                'key': item['key'],
                'title': item['title'],
                'score': item['score'],
                'label': labels_by_key[item['key']],
            }
            for item in baseline_scores
        ]

    def _normalize_about_user(self, value: Any) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise ValueError('about_user must be an object')
        age = self._require_non_empty_string(value.get('age'), 'about_user.age')
        experience = self._require_non_empty_string(value.get('experience'), 'about_user.experience')
        education = self._require_non_empty_string(value.get('education'), 'about_user.education')
        strengths = self._ensure_string_list(value.get('strengths'), field_name='about_user.strengths', min_items=1)
        return {
            'age': age,
            'experience': experience,
            'strengths': strengths,
            'education': education,
        }

    def _normalize_career_fit(self, value: Any) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise ValueError('career_fit must be an object')
        title = self._require_non_empty_string(value.get('title'), 'career_fit.title')
        summary = self._require_non_empty_string(value.get('summary'), 'career_fit.summary')
        professions = self._ensure_string_list(value.get('professions'), field_name='career_fit.professions', min_items=1)
        return {
            'title': title,
            'summary': summary,
            'professions': professions[:5],
        }

    def _normalize_development_recommendations(self, value: Any) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise ValueError('development_recommendations must be an object')
        title = self._require_non_empty_string(value.get('title'), 'development_recommendations.title')
        summary = self._require_non_empty_string(value.get('summary'), 'development_recommendations.summary')
        steps = self._ensure_string_list(value.get('steps'), field_name='development_recommendations.steps', min_items=3)
        return {
            'title': title,
            'summary': summary,
            'steps': steps[:3],
        }

    def _ensure_string_list(
        self,
        value: Any,
        *,
        field_name: str = 'list',
        min_items: int = 0,
    ) -> list[str]:
        if not isinstance(value, list):
            raise ValueError(f'{field_name} must be a list')
        items = [str(item).strip() for item in value if str(item).strip()]
        if len(items) < min_items:
            raise ValueError(f'{field_name} must contain at least {min_items} item(s), got {len(items)}')
        return items

    def _ensure_profession_list(self, value: Any) -> list[dict[str, Any]]:
        if not isinstance(value, list):
            raise ValueError('recommended_professions must be a list')

        normalized: list[dict[str, Any]] = []
        for item in value:
            if not isinstance(item, dict):
                continue
            name = str(item.get('name', '')).strip()
            rationale = str(item.get('rationale', '')).strip()
            fit_score = item.get('fit_score')
            if not name or not rationale:
                continue
            if not isinstance(fit_score, int):
                raise ValueError(f'recommended_professions["{name}"].fit_score must be an integer, got {type(fit_score).__name__}')
            if not 0 <= fit_score <= 100:
                raise ValueError(f'recommended_professions["{name}"].fit_score must be 0–100, got {fit_score}')
            normalized.append({'name': name, 'rationale': rationale, 'fit_score': fit_score})

        if not normalized:
            raise ValueError('recommended_professions must contain at least one valid item')
        return normalized

    def _require_non_empty_string(self, value: Any, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f'{field_name} must be a non-empty string, got {type(value).__name__}: {value!r}')
        return value.strip()


SCORE_LABELS_SYSTEM_PROMPT = """Ты помощник по профориентации для подростков и молодёжи 16–22 лет.

Тебе передаются результаты теста по 6 шкалам (key, title, score от 0 до 12).
Твоя задача — для каждой шкалы написать короткий, живой и понятный label на «ты».

Правила:
- Отвечай только JSON-массивом, без markdown и пояснений.
- Для каждого элемента верни только поля key и label.
- label — 1 предложение на русском, разговорный стиль, обращение на «ты».
- Не пересчитывай score и не придумывай числа.
- Если score низкий (0–4): скажи, что направление пока не близко.
- Если score средний (5–7): скажи, что есть интерес, но не основной.
- Если score высокий (8–12): скажи, что это сильная сторона.
- Не добавляй никакого текста вне JSON."""


class BothubAIScoreLabelsClient:
    """
    Лёгкий клиент только для генерации score labels на этапе anonymous submit.
    Не требует профиля пользователя.
    """

    def __init__(self) -> None:
        self.settings = get_settings()

    async def generate_score_labels(
        self,
        score_summary: list[dict[str, Any]],
    ) -> dict[str, str]:
        """
        Возвращает словарь {key: label} для всех шкал.
        Поднимает исключение при любой ошибке (вызывающий сам решает, делать fallback или нет).
        """
        if not self.settings.ai_api_key:
            raise RuntimeError('AI_API_KEY is not set')

        schema_example = [{'key': 'people', 'label': 'string'}, '...']
        user_message = (
            f'Схема ответа (верни строго этот JSON-массив):\n{json.dumps(schema_example, ensure_ascii=False)}\n\n'
            f'Результаты теста:\n{json.dumps(score_summary, ensure_ascii=False, indent=2)}'
        )

        payload = {
            'model': self.settings.ai_model,
            'messages': [
                {'role': 'system', 'content': SCORE_LABELS_SYSTEM_PROMPT},
                {'role': 'user', 'content': user_message},
            ],
            'temperature': 0.4,
        }
        headers = {
            'Authorization': f'Bearer {self.settings.ai_api_key}',
            'Content-Type': 'application/json',
        }

        async with httpx.AsyncClient(timeout=self.settings.ai_timeout_seconds) as client:
            response = await client.post(
                f"{self.settings.ai_base_url.rstrip('/')}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        content = data['choices'][0]['message']['content']
        if isinstance(content, list):
            content = ''.join(part.get('text', '') for part in content if isinstance(part, dict))

        return self._parse_labels(content, score_summary)

    def _parse_labels(self, raw_text: str, score_summary: list[dict[str, Any]]) -> dict[str, str]:
        raw_text = raw_text.strip()
        if raw_text.startswith('```'):
            raw_text = re.sub(r'^```(?:json)?', '', raw_text).strip()
            raw_text = re.sub(r'```$', '', raw_text).strip()

        # Ожидаем массив, но AI иногда оборачивает в объект
        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError:
            match = re.search(r'\[.*\]', raw_text, re.DOTALL)
            if not match:
                raise ValueError('AI score labels response does not contain a JSON array')
            parsed = json.loads(match.group(0))

        if isinstance(parsed, dict):
            # Иногда AI возвращает {"scores": [...]} — пробуем развернуть
            for v in parsed.values():
                if isinstance(v, list):
                    parsed = v
                    break

        if not isinstance(parsed, list):
            raise ValueError('AI score labels response is not a JSON array')

        labels: dict[str, str] = {}
        for item in parsed:
            if not isinstance(item, dict):
                continue
            key = str(item.get('key', '')).strip()
            label = str(item.get('label', '')).strip()
            if key and label:
                labels[key] = label

        expected_keys = {item['key'] for item in score_summary}
        missing = expected_keys - labels.keys()
        if missing:
            raise ValueError(f'AI score labels missing keys: {", ".join(sorted(missing))}')

        return labels
