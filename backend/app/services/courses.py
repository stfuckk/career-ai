"""
Клиент Stepik API для поиска курсов по навыкам из career_path.

Stepik API — публичный, без ключа.
GET https://stepik.org/api/courses?search={query}&page_size=N
Возвращает полные данные: название, описание, цена, длительность, рейтинг.
"""
import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

STEPIK_API_BASE = 'https://stepik.org/api'
STEPIK_COURSE_URL = 'https://stepik.org/course/{course_id}'


class StepikClient:
    def __init__(self, timeout: int = 15) -> None:
        self.timeout = timeout

    async def search_courses_for_career_path(
        self,
        career_path_steps: list[dict[str, Any]],
        per_skill: int = 2,
    ) -> dict[int, list[dict[str, Any]]]:
        results: dict[int, list[dict[str, Any]]] = {}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                for step_index, step in enumerate(career_path_steps):
                    skills = step.get('skills_to_learn', [])
                    if not skills:
                        continue

                    step_courses: list[dict[str, Any]] = []
                    seen_ids: set[int] = set()

                    for skill in skills:
                        skill_clean = str(skill).strip()
                        if not skill_clean:
                            continue

                        queries = self._build_queries(skill_clean, step)

                        for query in queries:
                            try:
                                courses = await self._search(client, query, per_skill)
                                logger.info('Stepik search for "%s" returned %d courses', query, len(courses))
                            except Exception:  # noqa: BLE001
                                logger.warning('Stepik search failed for query="%s"', skill_clean, exc_info=True)
                                continue

                            if not courses:
                                continue

                            for course in courses:
                                if course['stepik_course_id'] not in seen_ids:
                                    course['skill'] = skill_clean
                                    step_courses.append(course)
                                    seen_ids.add(course['stepik_course_id'])

                            break

                    if step_courses:
                        results[step_index] = step_courses

        except Exception:  # noqa: BLE001
            logger.warning('Stepik course search failed entirely', exc_info=True)
            return {}

        return results

    async def _search(
        self,
        client: httpx.AsyncClient,
        query: str,
        limit: int,
    ) -> list[dict[str, Any]]:
        response = await client.get(
            f'{STEPIK_API_BASE}/courses',
            params={
                'search': query,
                'page': 1,
            },
        )
        response.raise_for_status()
        data = response.json()

        courses = data.get('courses', [])
        return [self._normalize(c) for c in courses[:limit]]

    def _build_queries(self, skill: str, step: dict[str, Any]) -> list[str]:
        queries: list[str] = []

        skill_clean = skill.strip()
        if skill_clean:
            queries.append(skill_clean)

        # если есть скобки — достаём содержимое: (Python/JavaScript) -> Python, JavaScript
        if '(' in skill_clean and ')' in skill_clean:
            inside = skill_clean.split('(', 1)[1].rsplit(')', 1)[0]
            for part in inside.split('/'):
                part = part.strip()
                if part:
                    queries.append(part)

        lower = skill_clean.lower()

        replacements = {
            'работа с git': ['git'],
            'работа с базами данных': ['sql', 'базы данных'],
            'основы алгоритмов и структур данных': ['алгоритмы', 'структуры данных'],
            'базовый синтаксис языка (python/javascript)': ['python', 'javascript'],
            'фреймворки (django/react)': ['django', 'react'],
            'архитектура приложений': ['архитектура по', 'архитектура приложений'],
            'оптимизация кода': ['оптимизация кода'],
            'наставничество': ['лидерство', 'коммуникация'],
        }

        queries.extend(replacements.get(lower, []))

        title = str(step.get('title') or '').strip()
        if title:
            queries.append(title)

        hh_query = str(step.get('hh_search_query') or '').strip()
        if hh_query:
            queries.append(hh_query)

        # убираем дубли, сохраняя порядок
        unique_queries: list[str] = []
        seen: set[str] = set()
        for q in queries:
            q_norm = q.strip()
            if q_norm and q_norm not in seen:
                seen.add(q_norm)
                unique_queries.append(q_norm)

        return unique_queries

    def _extract_average_rating(self, course: dict[str, Any]) -> float | None:
        """
        Stepik может вернуть review_summary как dict, а может не вернуть его в раскрытом виде.
        В таком случае рейтинг безопаснее не заполнять, чем ронять весь поиск.
        """
        review_summary = course.get('review_summary')

        if isinstance(review_summary, dict):
            average = review_summary.get('average')
            if average is None:
                return None
            try:
                return round(float(average), 1)
            except (TypeError, ValueError):
                return None

        return None

    def _normalize(self, course: dict[str, Any]) -> dict[str, Any]:
        """Нормализует ответ Stepik API в наш формат."""
        course_id = course['id']
        price = course.get('price')
        currency = course.get('currency_code') or 'RUB'

        # time_to_complete приходит в секундах, конвертируем в часы
        time_seconds = course.get('time_to_complete')
        time_to_complete_hours = round(time_seconds / 3600) if time_seconds else None

        return {
            'stepik_course_id': course_id,
            'title': course.get('title', ''),
            'summary': (course.get('summary') or '').strip(),
            'url': STEPIK_COURSE_URL.format(course_id=course_id),
            'cover_url': course.get('cover') or None,
            'price': float(price) if price else None,
            'currency': currency if price else None,
            'is_free': not price or float(price) == 0,
            'time_to_complete_hours': time_to_complete_hours,
            'learners_count': course.get('learners_count') or 0,
            'total_units': course.get('total_units') or 0,
            'average_rating': self._extract_average_rating(course),
        }
