import json
import re
from typing import Any

import httpx

from app.core.config import get_settings


class BothubAIClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def analyze_test_result(
        self,
        *,
        profile_snapshot: dict[str, Any],
        score_summary: list[dict[str, Any]],
        methodology_text: str,
        methodology_json: dict[str, Any],
    ) -> dict[str, Any]:
        if not self.settings.ai_api_key:
            return self._fallback_response(score_summary)

        prompt = (
            'Ты помогаешь с профориентацией пользователям 16-22 лет. '
            'Тебе переданы профиль пользователя, уже рассчитанные баллы по методике, '
            'а также текст и структура методического документа. '
            'Не пересчитывай баллы заново, а опирайся на уже переданные результаты. '
            'Верни ТОЛЬКО JSON следующего формата: '
            '{"summary": "...", "recommended_professions": [{"name": "...", "rationale": "...", "fit_score": 0}], '
            '"hh_search_queries": ["..."], "preview_summary": "..."}. '
            'Профессии должны подходить для начинающих, стажеров, junior или без опыта. '
            f'Профиль: {json.dumps(profile_snapshot, ensure_ascii=False)}. '
            f'Подсчитанные баллы: {json.dumps(score_summary, ensure_ascii=False)}. '
            f'Текст методики: {methodology_text}. '
            f'Структура методики: {json.dumps(methodology_json, ensure_ascii=False)}.'
        )

        try:
            response = await self._chat_json(prompt)
            return self._normalize_response(response, score_summary)
        except Exception:
            return self._fallback_response(score_summary)

    async def _chat_json(self, prompt: str) -> dict[str, Any]:
        payload = {
            'model': self.settings.ai_model,
            'messages': [
                {'role': 'system', 'content': 'You must answer only with strict JSON.'},
                {'role': 'user', 'content': prompt},
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
                raise
            parsed = json.loads(match.group(0))
        if not isinstance(parsed, dict):
            raise ValueError('Parsed JSON is not an object')
        return parsed

    def _normalize_response(self, response: dict[str, Any], score_summary: list[dict[str, Any]]) -> dict[str, Any]:
        normalized = self._fallback_response(score_summary)
        normalized['summary'] = response.get('summary') or normalized['summary']
        normalized['preview_summary'] = response.get('preview_summary') or normalized['preview_summary']
        professions = self._ensure_profession_list(response.get('recommended_professions'))
        if professions:
            normalized['recommended_professions'] = professions
        queries = self._ensure_string_list(response.get('hh_search_queries'))
        if queries:
            normalized['hh_search_queries'] = queries
        return normalized

    def _ensure_string_list(self, value: Any) -> list[str]:
        if not isinstance(value, list):
            return []
        return [str(item).strip() for item in value if str(item).strip()]

    def _ensure_profession_list(self, value: Any) -> list[dict[str, Any]]:
        if not isinstance(value, list):
            return []
        normalized: list[dict[str, Any]] = []
        for item in value:
            if isinstance(item, str) and item.strip():
                normalized.append({'name': item.strip(), 'rationale': '', 'fit_score': 75})
                continue
            if not isinstance(item, dict):
                continue
            name = str(item.get('name', '')).strip()
            if not name:
                continue
            try:
                fit_score = max(0, min(100, int(item.get('fit_score', 75))))
            except (TypeError, ValueError):
                fit_score = 75
            normalized.append(
                {
                    'name': name,
                    'rationale': str(item.get('rationale', '')).strip(),
                    'fit_score': fit_score,
                }
            )
        return normalized

    def _fallback_response(self, score_summary: list[dict[str, Any]]) -> dict[str, Any]:
        top = sorted(score_summary, key=lambda item: item['score'], reverse=True)[:2]
        top_keys = [item['key'] for item in top]
        profession_map = {
            'people': [
                {'name': 'Специалист поддержки', 'rationale': 'Подходит при выраженной склонности к работе с людьми.', 'fit_score': 86},
                {'name': 'Ассистент преподавателя', 'rationale': 'Подходит тем, кому важно взаимодействие и помощь другим.', 'fit_score': 83},
                {'name': 'HR-ассистент', 'rationale': 'Требует коммуникации и умения находить общий язык с людьми.', 'fit_score': 80},
            ],
            'research': [
                {'name': 'Стажер-аналитик', 'rationale': 'Подходит при интересе к анализу и исследовательским задачам.', 'fit_score': 88},
                {'name': 'Лаборант-исследователь', 'rationale': 'Связано с экспериментами и научной деятельностью.', 'fit_score': 82},
                {'name': 'Junior QA analyst', 'rationale': 'Подходит при внимании к деталям и аналитическом мышлении.', 'fit_score': 79},
            ],
            'practical': [
                {'name': 'Техник-стажер', 'rationale': 'Подходит при интересе к практической работе и технике.', 'fit_score': 85},
                {'name': 'Монтажник-стажер', 'rationale': 'Связано с практической деятельностью и работой руками.', 'fit_score': 80},
                {'name': 'Помощник инженера', 'rationale': 'Дает прикладной старт в техническом направлении.', 'fit_score': 78},
            ],
            'aesthetic': [
                {'name': 'Графический дизайнер-стажер', 'rationale': 'Подходит при интересе к визуальному творчеству.', 'fit_score': 86},
                {'name': 'Контент-менеджер', 'rationale': 'Сочетает работу с визуалом и текстом.', 'fit_score': 80},
                {'name': 'SMM-ассистент', 'rationale': 'Подходит при интересе к креативным задачам.', 'fit_score': 78},
            ],
            'extreme': [
                {'name': 'Инструктор-стажер', 'rationale': 'Подходит тем, кому важна активность и работа в динамичной среде.', 'fit_score': 82},
                {'name': 'Спортивный организатор', 'rationale': 'Связано с активностью и мероприятиями.', 'fit_score': 77},
                {'name': 'Помощник координатора выездных мероприятий', 'rationale': 'Подходит для людей, которым нравятся нестандартные условия.', 'fit_score': 76},
            ],
            'economic': [
                {'name': 'Помощник бухгалтера', 'rationale': 'Подходит при склонности к расчетам и аккуратности.', 'fit_score': 86},
                {'name': 'Офис-ассистент', 'rationale': 'Хороший старт в работе с документами и организацией процессов.', 'fit_score': 80},
                {'name': 'Младший аналитик данных', 'rationale': 'Подходит при интересе к структуре, данным и планированию.', 'fit_score': 79},
            ],
        }

        recommended: list[dict[str, Any]] = []
        for key in top_keys:
            recommended.extend(profession_map.get(key, []))
        if not recommended:
            recommended = [
                {'name': 'Стажер', 'rationale': 'Базовая рекомендация для первого профориентационного шага.', 'fit_score': 70}
            ]

        hh_queries = [profession['name'] for profession in recommended[:3]]
        preview = 'Вам подходят направления: ' + ', '.join(item['title'].lower() for item in top)
        summary = (
            'По результатам теста наиболее выражены направления: '
            + ', '.join(item['title'].lower() for item in top)
            + '. Рекомендуется начать с базовых или стажерских ролей, чтобы проверить интерес на практике.'
        )
        return {
            'summary': summary,
            'recommended_professions': recommended[:6],
            'hh_search_queries': hh_queries,
            'preview_summary': preview,
        }
