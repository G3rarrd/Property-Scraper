from urllib.parse import quote
from typing import Optional
import re

from scraper_infrastructre.browser_manager import BrowserManager
from playwright.async_api import Page

class GoogleMapsGeocoder:

    @staticmethod
    def __build_search_url(address: str) -> str:
        return (
            "https://www.google.com/maps/search/"
            f"?api=1&query={quote(address)}"
        )
    
    @staticmethod
    def __extract_coordinates(coordinates_url) -> tuple[Optional[float], Optional[float]]:
        match = (re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', coordinates_url)
            or re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', coordinates_url)
        )

        if not match:
            return (None, None)
        
        latitude = float(match.group(1))
        longitude = float(match.group(2))

        return (latitude, longitude)

    async def __async_fetch_url(self, page: Page, url : str):
        response = await page.goto(url, wait_until="commit",  timeout=30000)
        await page.wait_for_function(
            "() => window.location.href.includes('/@')",
            timeout=30000
        )
        return page.url
    
    async def async_geocode(self, page: Page, address: str) -> tuple[Optional[float], Optional[float]]:
        url = self.__build_search_url(address)
        final_url = await self.__async_fetch_url(page=page, url=url)
        return self.__extract_coordinates(final_url)
