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
        normalized['recommended_professions'] = self._ensure_profession_list(response.get('recommended_professions')) or normalized['recommended_professions']
        normalized['hh_search_queries'] = self._ensure_string_list(response.get('hh_search_queries')) or normalized['hh_search_queries']
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
            fit_score = item.get('fit_score', 75)
            try:
                fit_score = max(0, min(100, int(fit_score)))
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
                {'name': 'Техник-стажер', 'rationale': 'Подходит тем, кто любит практическую деятельность и работу с техникой.', 'fit_score': 86},
                {'name': 'Монтажник-стажер', 'rationale': 'Связано с практическими навыками и изготовлением изделий.', 'fit_score': 78},
                {'name': 'Оператор производства', 'rationale': 'Подходит при ориентации на конкретный результат и практику.', 'fit_score': 76},
            ],
            'aesthetic': [
                {'name': 'Графический дизайнер-стажер', 'rationale': 'Подходит при интересе к визуальному и творческому самовыражению.', 'fit_score': 87},
                {'name': 'Контент-мейкер', 'rationale': 'Связано с творческой подачей идей и эстетическим вкусом.', 'fit_score': 82},
                {'name': 'SMM-ассистент', 'rationale': 'Подходит для творческих задач и работы с контентом.', 'fit_score': 79},
            ],
            'extreme': [
                {'name': 'Инструктор по спорту (ассистент)', 'rationale': 'Подходит при высокой тяге к активности и спортивной среде.', 'fit_score': 81},
                {'name': 'Помощник организатора мероприятий', 'rationale': 'Подходит тем, кто любит динамику и нестандартные условия.', 'fit_score': 77},
                {'name': 'Туристический ассистент', 'rationale': 'Подходит при интересе к поездкам и активности.', 'fit_score': 74},
            ],
            'economic': [
                {'name': 'Помощник бухгалтера', 'rationale': 'Подходит при интересе к расчетам, аккуратности и работе с документами.', 'fit_score': 86},
                {'name': 'Офис-ассистент', 'rationale': 'Подходит при склонности к планированию и делопроизводству.', 'fit_score': 80},
                {'name': 'Стажер-экономист', 'rationale': 'Связано с расчетами и системной работой с информацией.', 'fit_score': 78},
            ],
        }
        query_map = {
            'people': ['специалист поддержки стажер', 'hr ассистент', 'ассистент преподавателя'],
            'research': ['стажер аналитик', 'junior qa analyst', 'лаборант исследователь'],
            'practical': ['техник стажер', 'монтажник стажер', 'оператор производства без опыта'],
            'aesthetic': ['графический дизайнер стажер', 'smm ассистент', 'контент менеджер стажер'],
            'extreme': ['инструктор по спорту ассистент', 'помощник организатора мероприятий', 'туристический ассистент'],
            'economic': ['помощник бухгалтера', 'офис ассистент', 'стажер экономист'],
        }

        professions: list[dict[str, Any]] = []
        hh_search_queries: list[str] = []
        for key in top_keys:
            professions.extend(profession_map.get(key, []))
            hh_search_queries.extend(query_map.get(key, []))

        score_titles = ', '.join(f"{item['title']}: {item['score']}" for item in top)
        return {
            'summary': f"По результатам опроса наиболее выражены направления: {', '.join(item['title'] for item in top)}. Ключевые баллы: {score_titles}.",
            'preview_summary': 'Тест пройден. Мы определили ваши ведущие профессиональные склонности и сохранили результат.',
            'recommended_professions': professions[:6],
            'hh_search_queries': hh_search_queries[:6],
        }
