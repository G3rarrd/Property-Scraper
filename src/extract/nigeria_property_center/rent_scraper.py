from logging import Logger
from typing import Final
from infrastructre.browser_manager import AsyncBrowserManager
from logger import get_logger
from .producer import producer
from .rent_writer import npc_writer
from .rent_worker import worker
from .sort_listings import NPCSortListings
from asyncio import Queue
import asyncio
from pathlib import Path

URL : Final[str] = "https://nigeriapropertycentre.com/for-rent"
LOGGER : Logger = get_logger(__name__)

async def sort_listings_process(headless : bool = False):
    # Warmup and Sort listings  
    sort_listings_browser : AsyncBrowserManager = AsyncBrowserManager("npc_rent_session.json", headless)
    
    await sort_listings_browser.start()
    
    LOGGER.info(
        "Browser Started | Sorting Listings",
        extra={
            "event": "browser_started",
            "headless": sort_listings_browser._headless,
        }
    )
    
    sort_listings = NPCSortListings(sort_listings_browser)
    
    await sort_listings.run(URL)
    
    await sort_listings_browser.close()

async def scrape_write_process(
    data_dir : Path, 
    num_workers :int, 
    start_page : int, 
    end_page : int
):
    
    npc_scraper_browser : AsyncBrowserManager = AsyncBrowserManager("npc_rent_session.json", False)
    
    await npc_scraper_browser.start()
    
    input_queue : Queue = Queue()
    result_queue : Queue = Queue()
    
    workers = [
            asyncio.create_task(
                worker(
                    f"worker={i}",
                    npc_scraper_browser,
                    input_queue,
                    result_queue
                )
            )
            for i in range(num_workers)
        ]
    
    writer_task = asyncio.create_task(
            npc_writer(result_queue, data_dir)
        )
    
        # producer
    await producer(URL, input_queue, start_page, end_page)
    
    # poison workers
    for _ in range(num_workers):
        await input_queue.put(None)

    await writer_task


    await input_queue.join()

    await asyncio.gather(*workers)

    await npc_scraper_browser.close()

    

async def run_scraper(
        data_dir : Path, 
        start_page : int, 
        end_page : int,
        num_workers : int = 3
    ):
    # await sort_listings_process()
    
    await scrape_write_process(data_dir, num_workers, start_page, end_page)