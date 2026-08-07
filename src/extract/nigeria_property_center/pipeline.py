from ...scrape.nigeria_property_center.rent_scraper import run_scraper
from src.config.npc_paths import RAW_RENTAL
from pathlib import Path

from src.config.settings import settings

async def pipeline():
    RAW_RENTAL.parent.mkdir(parents=True, exist_ok=True)
    
    # await run_scraper(RAW_RENTAL,settings.start_page,settings.end_page,settings.worker_count)
    
    print(len(list(RAW_RENTAL.glob("*.html.gz"))))