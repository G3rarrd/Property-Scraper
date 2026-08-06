from .rent_scraper import run_scraper
from src.config.npc_paths import RAW_RENTAL_LISTINGS
from pathlib import Path

from src.config.settings import settings

async def pipeline():
    RAW_RENTAL_LISTINGS.parent.mkdir(parents=True, exist_ok=True)
    
    await run_scraper(
        RAW_RENTAL_LISTINGS,
        settings.start_page,
        settings.end_page,
        settings.worker_count
    )