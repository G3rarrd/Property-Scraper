from logging import Logger
from typing import Final
from src.scraper_infrastructre.browser_manager import AsyncBrowserManager
from src.logger import get_logger
from .url_producer import producer
from ...extract.nigeria_property_center.rent_writer import rent_writer
from .rent_worker import worker
from .sort_listings import NPCSortListings
from asyncio import Queue
import asyncio
from pathlib import Path

URL : Final[str] = "https://nigeriapropertycentre.com/for-rent"
LOGGER : Logger = get_logger(__name__)



async def run_scraper(data_dir : Path, start_page : int, end_page : int, num_workers : int = 3):
    npc_scraper_browser : AsyncBrowserManager = AsyncBrowserManager("npc_rent_session.json", False)
        
    await npc_scraper_browser.start()
    
    input_queue : Queue = Queue()

    workers = [
            asyncio.create_task(
                worker(
                    f"worker={i}",
                    npc_scraper_browser,
                    input_queue,
                    data_dir
                )
            )
            for i in range(num_workers)
        ]
    
    await producer(URL, input_queue, start_page, end_page)
    
    # poison workers
    for _ in range(num_workers):
        await input_queue.put(None)
        
    await input_queue.join()

    await asyncio.gather(*workers)

    await npc_scraper_browser.close()