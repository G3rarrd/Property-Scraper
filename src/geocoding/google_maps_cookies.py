import json

from src.config.paths import SESSION_DIR
from src.fetchers.playwright.playwright import PlaywrightFetcher
from src.fetchers.playwright.playwright_config import PlaywrightConfig
from playwright.async_api import Page, Cookie

DEBUG = False

class GoogleMapsCookieManger:
    def __init__(self, filename : str):
        self.filepath = SESSION_DIR / f"{filename}.json"
        self._cookies = None

    async def solve_google_maps_cookies(self) -> list[Cookie]:
        headless = not DEBUG
        
        plw_config : PlaywrightConfig = PlaywrightConfig(headless=headless)
        playwright : PlaywrightFetcher =  PlaywrightFetcher(plw_config)
        
        await playwright.start()
        
        url : str = "https://www.google.com/maps"
        page : Page = await playwright.context.new_page()
        
        await page.goto(url, wait_until="domcontentloaded")
        
        if 'consent' in page.url:
            await page.click("button:has-text('Accept all')")
        
        self._cookies = await playwright.context.cookies()
        
        await playwright.close()

    def save_cookies(self):
        with open(self.filepath, "w", encoding="utf-8") as fw:
            data = json.dumps(self._cookies, indent=2)
            fw.write(data)
        
    def get_cookies(self):
        with open(self.filepath, "r", encoding="utf-8") as fr:
            data = json.loads(fr.read())
            return {c["name"]: c["value"] for c in data}