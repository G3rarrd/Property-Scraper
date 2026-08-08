from logging import Logger
from typing import Final
# from src.fetchers.base import Fetcher
from src.fetchers.curl.curl import CurlFetcher
# from src.fetchers.playwright.playwright import PlaywrightFetcher
# from src.fetchers.playwright.playwright_config import PlaywrightConfig
from src.logger import get_logger
from ...extract.nigeria_property_center.rent_writer import rent_writer
from .npc_worker import worker

from asyncio import Queue
import asyncio
from pathlib import Path

URL : Final[str] = "https://nigeriapropertycentre.com/for-rent"
LOGGER : Logger = get_logger(__name__)

async def run_scraper(data_dir : Path, url_list : list[str], num_workers : int = 3):
    input_queue : Queue = Queue()
    
    workers = [
            asyncio.create_task(
                worker(
                    f"worker={i}",
                    CurlFetcher(),
                    input_queue,
                    data_dir
                )
            )
            for i in range(num_workers)
        ]
    
    for url in url_list:
        await input_queue.put(url)
    
    # poison workers
    for _ in range(num_workers):
        await input_queue.put(None)
        
    await input_queue.join()

    await asyncio.gather(*workers)