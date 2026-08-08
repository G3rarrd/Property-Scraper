from asyncio import Queue
from pathlib import Path
from src.fetchers.base import Fetcher
from src.fetchers.playwright.browser_manager import AsyncBrowserManager
from src.utils.url_parser import get_page_number
from ...extract.nigeria_property_center.rent_model import RentField
from ...extract.nigeria_property_center.rent_parser import parse_property
from .html_writer import archive_html
from src.logger import get_logger, Logger
import asyncio

LOGGER : Logger = get_logger(__name__)
lock = asyncio.Lock()
async def worker(
        name : str, 
        fetcher : Fetcher,
        input_queue : Queue, 
        output_dir : Path
    ):

    LOGGER.info(
        f"{name} started",
        extra={
            "event": "worker_started",
            "worker": name,
        },
    )

    
    saved_count = 0
    await fetcher.start()
    

    while True:
        url : str = await input_queue.get()
        
        if url is None:
            input_queue.task_done()
            await fetcher.close()
            break
            
        try:
            page_number : int = 0
            async with lock:
                page_number = get_page_number(url)
                
            result = await fetcher.get(url)
            
            content = result.content
            status_code = result.status_code
            
            LOGGER.info(
                f"URL : {url} | Status Code : {status_code } | {name}",
                extra={
                    "event": "response",
                    "url" : url,
                    "status_code" : status_code 
                }
            )
            
            output_html_path = await archive_html(content , page_number, output_dir)
            
            saved_count += 1
            
            LOGGER.info(
                f"Archived Page : {page_number} | Saved to: {output_html_path} | {name} | Total saved: {saved_count}",
                extra={
                    "event": "html_archived",
                    "url": url,
                    "output_path": output_html_path,
                    "worker": name,
                    "total_saved": saved_count
                },
            )

        finally:
            input_queue.task_done()

    

