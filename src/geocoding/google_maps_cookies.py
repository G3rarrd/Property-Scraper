import json

from src.config.paths import SESSION_DIR
from src.fetchers.playwright.playwright import PlaywrightFetcher
from src.fetchers.playwright.playwright_config import PlaywrightConfig
from playwright.async_api import Page, Cookie

DEBUG = False

import logging

logger = logging.getLogger(__name__)
class GoogleMapsCookieManger:
    def __init__(self, filename : str):
        self.filepath = SESSION_DIR / f"{filename}.json"
        self._cookies = None

    async def solve_google_maps_cookies(self, retries: int = 5) -> list[Cookie]:
        headless = not DEBUG
        plw_config = PlaywrightConfig(headless=headless)
        playwright = PlaywrightFetcher(plw_config)

        await playwright.start()
        url = "https://www.google.com/maps"

        try:
            page: Page = await playwright.context.new_page()

            for attempt in range(1, retries + 1):
                logger.info("[%d/%d] Loading Google Maps...", attempt, retries)
                try:
                    await page.goto(url, wait_until="domcontentloaded")

                    if "consent" in page.url:
                        # Resilient locator for consent buttons across various locales
                        accept_button = page.locator(
                            "button:has-text('Accept all'), button:has-text('I agree'), form[action*='consent'] button"
                        ).first
                        await accept_button.click()
                        await page.wait_for_load_state("networkidle")
                        logger.info("[%d/%d] Consent accept button clicked.", attempt, retries)
                    else:
                        logger.info("[%d/%d] Direct access granted (no consent screen detected).", attempt, retries)

                    self._cookies = await playwright.context.cookies()
                    logger.info("[%d/%d] Successfully captured %d cookies.", attempt, retries, len(self._cookies))
                    return self._cookies

                except Exception as e:
                    logger.warning("[%d/%d] Failed to solve cookies: %s", attempt, retries, e)

            logger.error("Exhausted all %d retries without capturing cookies.", retries)
            return []

        finally:
            await playwright.close()

    def save_cookies(self):
        if not self._cookies:
            logger.warning("No cookies available to save to %s", self.filepath)
            return
        
        with open(self.filepath, "w", encoding="utf-8") as fw:
            data = json.dumps(self._cookies, indent=2)
            fw.write(data)
            logger.info("Saved %d cookies to %s", len(self._cookies), self.filepath)
        
    def get_cookies(self):
        if not self.filepath.exists():
            logger.warning("Cookie file not found at %s", self.filepath)
            return {}
        
        with open(self.filepath, "r", encoding="utf-8") as fr:
            data = json.loads(fr.read())
            return {c["name"]: c["value"] for c in data}