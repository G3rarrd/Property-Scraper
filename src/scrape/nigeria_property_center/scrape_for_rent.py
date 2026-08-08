from src.config.settings import settings
from src.config.npc_paths import RAW_RENTAL
from src.config.npc_settings import RENT_START_PAGE, RENT_END_PAGE
from src.scrape.nigeria_property_center.npc_url_producer import npc_url_producer
from src.scrape.nigeria_property_center.npc_scraper import run_scraper
import asyncio


async def scrape_for_rent():
    rent_urls : list[str] = npc_url_producer("for-rent", RENT_START_PAGE, RENT_END_PAGE)
    await run_scraper(RAW_RENTAL, rent_urls, settings.worker_count)
    
if "__main__" == __name__:
    asyncio.run(scrape_for_rent())
    
    