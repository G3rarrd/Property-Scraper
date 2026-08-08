from src.extract.json_writer import write_to_json
from .rent_writer import rent_writer
from src.storage.html_loader import HTMLLoader

from ...scrape.nigeria_property_center.npc_scraper import run_scraper
from src.config.npc_paths import EXTRACTED_RENTAL_FILE, RAW_RENTAL
from pathlib import Path

from src.config.settings import settings

async def pipeline():
    # Scrape site
    RAW_RENTAL.parent.mkdir(parents=True, exist_ok=True)
    await run_scraper(RAW_RENTAL,settings.start_page,settings.end_page,settings.worker_count)
    
    # Parse html and extract property info
    loader = HTMLLoader()
    
    properties = rent_writer(loader, RAW_RENTAL)
    
    write_to_json(EXTRACTED_RENTAL_FILE, properties)
    print(len(list(RAW_RENTAL.glob("*.html.gz"))))