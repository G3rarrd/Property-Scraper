from playwright.async_api import Page, Response
from lxml import html
from typing import Optional

from logger import get_logger, Logger
LOGGER : Logger = get_logger(__name__)

async def extract_property_cards(page : Page, url : str) -> list:
    try:
        response : Optional[Response] = await page.goto(url, wait_until="domcontentloaded", timeout=300000)

        if response is None:
            return []

        content = await page.content()

        tree = html.fromstring(content)
        
        property_cards = tree.xpath("//article[contains(@class,'group')]")

        return property_cards
    
    except Exception as e:
        return []