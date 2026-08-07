from asyncio import Queue
from pathlib import Path
from src.scraper_infrastructre.browser_manager import AsyncBrowserManager
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
        browser_manager : AsyncBrowserManager, 
        input_queue : Queue, 
        output_dir : Path
        # result_queue: Queue[RentField], 
    ):

    LOGGER.info(
        f"{name} started",
        extra={
            "event": "worker_started",
            "worker": name,
        },
    )

    context, page = await browser_manager.create_page([])
    
    saved_count = 0
    
    try:
        while True:

            url : str = await input_queue.get()
            # print(url)
            if url is None:
                input_queue.task_done()
                break
                
            try:    
                async with lock:
                    page_number = get_page_number(url)
                
                output_html_path = await archive_html(page, page_number, url, output_dir)
                
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
                
                # properties_count : int = len(properties)
                # parsed : RentField | None = None
                
                # for prop in properties:
                #     parsed = parse_property(prop)
                #     await result_queue.put(parsed)
                    
                # if parsed:
                #     parsed_property_count = len([p for p in properties if p != None])
                #     LOGGER.info(
                #         f"{parsed_property_count}/{properties_count} properties parsed | {url} |{name} ",
                #         extra={
                #             "event": "properties_parsed",
                #             "worker": name,
                #             "property_url": url,
                #             "parsed_count": parsed_property_count,
                #             "properties_count": properties_count
                #         },
                #     )

            finally:
                input_queue.task_done()

    finally:
        await context.close()