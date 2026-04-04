from typing import Any

import httpx

from app.core.config import get_settings


class HeadHunterClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def search_vacancies(self, *, queries: list[str], page_size: int | None = None) -> list[dict[str, Any]]:
        normalized_queries = [q.strip() for q in queries if q and q.strip()]
        if not normalized_queries:
            return []

        headers = {'User-Agent': self.settings.hh_user_agent}
        if self.settings.hh_api_token:
            headers['Authorization'] = f'Bearer {self.settings.hh_api_token}'

        items: list[dict[str, Any]] = []
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                for query in normalized_queries[:3]:
                    params = {
                        'text': query,
                        'per_page': page_size or self.settings.hh_per_page,
                        'experience': 'noExperience',
                        'order_by': 'publication_time',
                    }
                    response = await client.get(
                        f"{self.settings.hh_base_url.rstrip('/')}/vacancies",
                        params=params,
                        headers=headers,
                    )
                    response.raise_for_status()
                    payload = response.json()
                    items.extend(payload.get('items', []))
        except Exception:
            return []

        deduplicated: dict[str, dict[str, Any]] = {}
        for item in items:
            deduplicated[item['id']] = {
                'hh_vacancy_id': item['id'],
                'title': item.get('name'),
                'employer_name': (item.get('employer') or {}).get('name'),
                'area_name': (item.get('area') or {}).get('name'),
                'salary_from': ((item.get('salary') or {}).get('from')),
                'salary_to': ((item.get('salary') or {}).get('to')),
                'currency': ((item.get('salary') or {}).get('currency')),
                'alternate_url': item.get('alternate_url') or '',
                'snippet': item.get('snippet'),
            }
        return [item for item in deduplicated.values() if item['alternate_url']][: self.settings.hh_per_page]
