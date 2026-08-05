import asyncio
from playwright.async_api import Page, BrowserContext
from infrastructre.browser_manager import AsyncBrowserManager
from typing import Any, Optional

from logger import get_logger, Logger

LOGGER : Logger = get_logger(__name__)

class NPCSortListings:
    SORT_MOST_RECENT = "2"

    def __init__(self, browser: AsyncBrowserManager,):
        self.__browser = browser

    async def _wait_for_listings(self, page: Page, url : str) -> None:
        await page.wait_for_selector(
            "article, div[class*='property'], a[aria-label]",
            state="visible",
            timeout=30000,
        )
        
    async def _is_most_recent_selected(self, page: Page, sort_button: Any) -> bool:
        text = await sort_button.text_content()
        
        if "Most Recent" in text:
            return True
        
        return False

    async def _apply_sort_most_recent(self, page: Page, url: str) -> None:
        sort_button = page.locator("button:has-text('Sort:')")
        
        await page.goto(
            url,
            wait_until="domcontentloaded",
        )

        if await self._is_most_recent_selected(page, sort_button):
            
            LOGGER.info(
                "Listings Already Sorted", 
                extra={"event": "listings_sorted_already"}
            )
            return
        
        await sort_button.click()

        async with page.expect_navigation():
            await page.locator(
                "a[role='menuitem'][data-sort-nav='2']"
            ).click()

        LOGGER.info(
            "Applying Sort Most Recent",
            extra={
                "event": "applying_sort_most_recent",
                "url": url,
                "sort_type": "most_recent",
            },
        )

        # await self._wait_for_listings(page, url)

        LOGGER.info(
            "Sort Flow Completed",
            extra={
                "event": "sort_flow_completed",
                "url": url,
            },
        )

    async def run(self, url: str):
        context = await self.__browser.new_context()

        try:
            page = await context.new_page()
            
            # LOGGER.info(
            #     "Starting listing sort",
            #     extra={
            #         "event": "listing_sort_started",
            #         "url": url,
            #     },
            # )
            
            await self._apply_sort_most_recent(page, url)
            
            await self.__browser.save_session(context)
            
        except Exception:
            LOGGER.exception(
                "Listing sort failed",
                extra={"event": "listing_sort_failed", "url": url},
            )
            raise

        finally:
            await context.close()