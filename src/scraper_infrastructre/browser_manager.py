from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Playwright
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import random
from src.scraper_infrastructre.browser_config import BROWSER_CONFIG
from src.logger import get_logger, Logger

LOGGER : Logger = get_logger(__name__)

class AsyncBrowserManager:
    def __init__(
            self,
            session_file: str,
            headless: bool = True,
    ):
        self._playwright : Optional[Playwright]  = None
        self._browser: Optional[Browser] = None

        self.session_file = Path("session_files") / session_file
        self.session_file.parent.mkdir(exist_ok=True)

        self._headless : bool = headless

        self._profiles : List[Dict[str, str]] = BROWSER_CONFIG.profiles
        self._viewports : List[Tuple[int, int]] = BROWSER_CONFIG.viewports

    async def start(self):
        self._playwright = await async_playwright().start()

        self._browser = await self._playwright.chromium.launch(
            headless=self._headless,
            args=BROWSER_CONFIG.args
        )


    def __random_scroll(self) -> None:
        if random.random() < 0.3:
            self.__page.mouse.wheel(
                0,
                random.randint(300, 1200)
            )

            self.__page.wait_for_timeout(
                random.randint(500, 750)
            )

    def __modify_browser_fingerprint(page : Page):
        page.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false
            });
                                     
            // Modify Platform
                                     
            Object.defineProperty(navigator, 'platform', {
                get : () => 'Win32'
            });
            
            // Override hardware concurrency
            Object.defineProperty(navigator, 'hardwareConcurrency', {
                get: () => 8
            });
                                     
            // Modify memory info
            Object.defineproperty(navigator, 'deviceMemory', {
                get: () => 8             
            });
        """)

    async def new_context(self) -> BrowserContext:
        if not self._browser:
            LOGGER.error(
                "browser_not_started",
                extra={
                    "event": "browser_not_started",
                },
            )
            raise RuntimeError("Browser not started. Call start().")
        
        profile : Dict[str, str] = random.choice(self._profiles)
        viewport : Tuple[int, int] = random.choice(self._viewports)

        context_kwargs = {
            "user_agent": profile["user_agent"],
            "locale": profile["locale"],
            "viewport": {
                "width": viewport[0],
                "height": viewport[1],
            },
            "timezone_id": BROWSER_CONFIG.timezone,
            # "permissions":[],
            # "extra_http_headers":{}
        }

        has_session : bool = self.session_file.exists()

        if has_session:
            context_kwargs["storage_state"] = str(self.session_file)

            LOGGER.info(
                "Session Loaded",
                extra={
                    "event": "session_loaded",
                    "session_file": str(self.session_file),
                },
            )

        context : BrowserContext = await self._browser.new_context(**context_kwargs)

        LOGGER.info(
            "Context Created",
            extra={
                "event" : "context_created"
            },
        )

        return context 

    async def create_page(self, resources : List[str]) -> Tuple[BrowserContext, Page]:
        LOGGER.info(
            "create_page_started",
            extra={
                "event": "create_page_started",
                "resource_blocking": bool(resources),
                "blocked_resources": resources,
            },
        )
        try:
            context = await self.new_context()

            async def block_resources(route):
                if route.request.resource_type in resources:
                    await route.abort()
                else:
                    await route.continue_()

            if resources:
                await context.route("**/*", block_resources)

                LOGGER.info(
                    "Resource Blocking Enabled",
                    extra={
                        "event": "resource_blocking_enabled",
                        "blocked_resources": resources,
                    },
                )

            page = await context.new_page()

            LOGGER.info("Page Created", extra={"event" : "page_created"})

            return context, page

        except Exception as e:
            LOGGER.exception(
                "Page Creation Failed",
                extra={
                    "event": "create_page_failed",
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "blocked_resources": resources,
                },
            )

        
    
    async def save_session(self, context: BrowserContext) -> None:
        LOGGER.info(
            "Saving Session",
            extra={
                "event" : "saving_session", 
                "path" : str(self.session_file)
            }
        )

        await context.storage_state(path=str(self.session_file))

    async def close(self) -> None:
        if self._browser:
            LOGGER.info(
                "Browser Closed", 
                extra={
                    "event": "browser_closed"
                }
            )
            await self._browser.close()

        if self._playwright:
            await self._playwright.stop()

        

    