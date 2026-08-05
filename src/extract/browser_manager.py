from playwright.sync_api import sync_playwright, Page
import random
from logging import Logger
from typing import Final, Optional
from pathlib import Path
import time

class BrowserManger:
    SESSION_FILE = "npc_session.json"
    SORT_MOST_RECENT = "2"
    DEFAULT_TIMEOUT = 240000
    HEADERS_POOL : Final[list[dict[str, str]]] = [
        {
            "name": "windows_chrome_us",
            "user_agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/136.0.0.0 Safari/537.36"
            ),
            "locale": "en-US",
        },
        {
            "name": "windows_chrome_uk",
            "user_agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/136.0.0.0 Safari/537.36"
            ),
            "locale": "en-GB",
        },
        {
            "name": "windows_edge",
            "user_agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/136.0.0.0 Safari/537.36 "
                "Edg/136.0.0.0"
            ),
            "locale": "en-US",
        },
        {
            "name": "macos_chrome",
            "user_agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/136.0.0.0 Safari/537.36"
            ),
            "locale": "en-US",
        },
        {
            "name": "linux_chrome",
            "user_agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/136.0.0.0 Safari/537.36"
            ),
            "locale": "en-US",
        },
    ]


    DIMENSIONS : Final[list[tuple[int, int]]] = [
        (1920, 1080),
        (1280, 720),
        (1366, 768)
    ]

    def __init__(self, logger : Logger, headless : bool = True):
        self.playwright = sync_playwright().start()
        self.__logger = logger

        self.profile = random.choice(self.HEADERS_POOL)
        self.viewport = random.choice(self.DIMENSIONS)

        
        self.__browser = self.playwright.chromium.launch(
            headless=headless,
            args=["--disable-blink-features=AutomationControlled"]
        )

        self.__context = self.__create_context()

        self.__page = self.__context.new_page()

        self.__page.set_default_timeout(self.DEFAULT_TIMEOUT)

        self.__logger.info(
            f"Browser started | {self.profile['name']} | {self.viewport}"
        )

    
    def __create_context(self):
        context_kwargs = {
            "user_agent": self.profile["user_agent"],
            "locale": self.profile["locale"],
            "viewport": {
                "width": self.viewport[0],
                "height": self.viewport[1],
            },
            "timezone_id": "Africa/Lagos",
            "permissions":[],
            "extra_http_headers":{}
        }

        if Path(self.SESSION_FILE).exists():
            context_kwargs["storage_state"] = self.SESSION_FILE

        return self.__browser.new_context(**context_kwargs)





    
    # def __start_browser(self, headless : bool) :
    #     with sync_playwright() as p:
    #         browser = p.chromium.launch(
    #             headless=headless,
    #             args=[
    #                 '--disable-blink-features=AutomationControlled',
    #                 '--disable-infobars',
    #                 '--disable-blink-features',
    #                 '--disable-blink-features=AutomationControlled'
    #             ]
    #         )

        # self.__browser = 


    


    
    def fetch(self, url: str) -> Optional[str]:
        self.__logger.info(f"Fetching: {url}")

        response = self.__page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=self.DEFAULT_TIMEOUT
        )

        content : str = self.__page.content()

        if response.status == 200:
            self.__logger.info(f"Fetched successfully ({response.status})")
            self.__random_scroll() 
        
        elif response.status == 403:
            self.__logger.error(f"Block detected ({response.status})")

        return content
    
    def close(self):
        self.__context.storage_state(
            path=self.SESSION_FILE
        )
        self.__browser.close()
        self.playwright.stop()
        