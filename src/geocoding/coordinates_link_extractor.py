from urllib.parse import quote
from typing import Optional
import re
from playwright.async_api import Page

class CoordinatesLinkExtractor:

    @staticmethod
    def _build_search_url(address: str) -> str:
        return (
            "https://www.google.com/maps/search/"
            f"?api=1&query={quote(address)}"
        )
    
    @staticmethod
    def _extract_coordinates(coordinates_url) -> tuple[Optional[float], Optional[float]]:
        match = (re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', coordinates_url)
            or re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', coordinates_url)
        )

        if not match:
            return (None, None)
        
        latitude = float(match.group(1))
        longitude = float(match.group(2))

        return (latitude, longitude)

    async def _get_url_with_coordinates(self, page: Page, url : str):
        response = await page.goto(url, wait_until="commit",  timeout=300000)
        await page.wait_for_function(
            "() => window.location.href.includes('/@')",
            timeout=300000
        )
        return page.url
    
    async def geocode(self, page: Page, address: str) -> tuple[Optional[float], Optional[float]]:
        url = self._build_search_url(address)
        final_url = await self._get_url_with_coordinates(page=page, url=url)
        return self._extract_coordinates(final_url)
