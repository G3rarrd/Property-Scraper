from dataclasses import dataclass
from typing import List, Tuple, Dict


@dataclass(frozen=True)
class BrowserConfig:
    timeout: int
    timezone: str
    profiles: List[Dict[str, str]]
    viewports: List[Tuple[int, int]]
    args : List[str]
    


BROWSER_CONFIG = BrowserConfig(
    timeout=240000,
    timezone="Africa/Lagos",
    profiles=[
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
        }
    ],

    viewports=[    
        (743,  587),
        (852,  687),
        (1280, 720),
        (1366, 768)
    ],
    
    args=["--disable-blink-features=AutomationControlled"]
)