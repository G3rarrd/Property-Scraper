from asyncio import Queue
from src.infrastructre.browser_manager import AsyncBrowserManager
from .rent_parser import parse_property
from .rent_property_extractor import extract_property_cards
from src.logger import get_logger, Logger

LOGGER : Logger = get_logger(__name__)

async def worker(
        name : str, 
        browser_manager : AsyncBrowserManager, 
        input_queue : Queue, 
        result_queue: Queue, 
    ):

    LOGGER.info(
        f"{name} started",
        extra={
            "event": "worker_started",
            "worker": name,
        },
    )

    context, page = await browser_manager.create_page([])
    
    processed_count = 0
    
    try:
        while True:

            url : str = await input_queue.get()
            # print(url)
            if url is None:
                
                LOGGER.info(
                    f"{name} Stopped | Processed Count: {processed_count}",
                    extra={
                        "event": "worker_stopped",
                        "worker": name,
                        "processed_count": processed_count,
                    },
                )
                input_queue.task_done()
                
                # kills the writer task
                if input_queue.empty():
                    await result_queue.put(None)
                
                break
                
            try:
                properties : list = await extract_property_cards(page, url)
                properties_count : int = len(properties)
                parsed = None
                
                for prop in properties:
                    parsed = parse_property(prop)
                    await result_queue.put(parsed)
                    
                if parsed:
                    parsed_property_count = len([p for p in properties if p != None])
                    LOGGER.info(
                        f"{parsed_property_count}/{properties_count} properties parsed | {url} |{name} ",
                        extra={
                            "event": "properties_parsed",
                            "worker": name,
                            "property_url": url,
                            "parsed_count": parsed_property_count,
                            "properties_count": properties_count
                        },
                    )

                processed_count += 1

            except Exception as e:
                LOGGER.exception(
                    f"URL Processing Failed | {name} | URL: {url} | Error: {e}",
                    extra={
                        "event": "url_processing_failed",
                        "worker": name,
                        "url": url,
                        "error_type": type(e).__name__,
                        "error_message": str(e),
                    },
                )

            finally:
                
                input_queue.task_done()

    finally:
        await context.close()