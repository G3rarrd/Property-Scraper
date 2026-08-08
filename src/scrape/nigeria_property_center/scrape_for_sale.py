from src.config.settings import settings
from src.config.npc_paths import RAW_RENTAL, RAW_SALE
from src.config.npc_settings import SALE_END_PAGE, SALE_START_PAGE
from src.scrape.nigeria_property_center.npc_url_producer import npc_url_producer
from src.scrape.nigeria_property_center.npc_scraper import run_scraper
import asyncio


async def scrape_for_sale():
    sale_urls : list[str] = npc_url_producer("for-sale", SALE_START_PAGE, SALE_END_PAGE)
    await run_scraper(RAW_SALE, sale_urls, settings.worker_count)
    
if "__main__" == __name__:
    asyncio.run(scrape_for_sale())