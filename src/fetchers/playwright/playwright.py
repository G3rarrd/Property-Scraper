from src.fetchers.base import FetchResult, Fetcher
from random import choice
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Cookie

from src.fetchers.playwright.playwright_config import PlaywrightConfig

import asyncio

class PlaywrightFetcher(Fetcher):
    def __init__(self, config : PlaywrightConfig):
        self.config = config
        self.headless = config.headless
        self.playwright = None
        
        self.playwright : PlaywrightFetcher | None = None
        self.browser : Browser | None = None
        self.context : BrowserContext | None = None
        
    async def start(self):
        if self.playwright:
            print("Playwright already started")
            return
        
        self.playwright = await async_playwright().start()
        
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless
        )
        
        self.context = await self.browser.new_context()
        
    async def close(self):
        if self.browser:
            await self.browser.close()
            self.browser = None
            self.context = None
        
            
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None
            
    async def create_page(self):
        return await self.context.new_page()
            
            
    async def get(self, url : str, **kwargs) -> FetchResult:
        if not self.context:
            raise("No Context Found. Start Playwright")
        
        page : Page = await self.context.new_page()
        
        response = await page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=self.config.timeout
        )
        
        content = await page.content()
        
        status_code = (response.status if response else 0)
        
        await page.close()
        
        return FetchResult(
            url=page.url,
            status_code=status_code,
            content=content
        )
        
    async def save_session(self):
        if self.context:
            self.context.storage_state()
        
async def demo():
    pass

    # res = await playwright.get(url)
    # print(res.url)
    # params = parse_qs(urlparse(res.url).query)

    # maps_url = params["continue"][0]

    # print(maps_url)
    # await playwright.close()
    
if "__main__" == __name__:
    asyncio.run(demo())