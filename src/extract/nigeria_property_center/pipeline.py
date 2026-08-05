from .rent_scraper import run_scraper
from config.paths import DATA_DIR
from pathlib import Path

from config.settings import settings

async def pipeline():
    npc_data_dir : Path = DATA_DIR / "nigeria_property_center" / "rent"
    
    npc_output_file : Path = npc_data_dir / "rental_listings.jsonl"
    
    npc_data_dir.mkdir(parents=True, exist_ok=True)
    
    await run_scraper(
        npc_output_file, 
        settings.start_page, 
        settings.end_page, 
        settings.worker_count
    )