from asyncio import Queue
# from geocoding.google_map_geocoder import GoogleMapsGeocoder
from typing import List

from src.fetchers.playwright.browser_manager import AsyncBrowserManager
from .google_map_geocoder import GoogleMapsGeocoder


async def worker(
        name : str, 
        browser_manager : AsyncBrowserManager, 
        geocoder : GoogleMapsGeocoder, 
        input_queue: Queue, 
        result_queue : Queue,
    ):
    print(f"[{name}] Starting")

    # Persistent Browser Context
    block_resources : List[str] =c
    context, page = await browser_manager.create_page(block_resources)
    
    try:
        while True:
            address = await input_queue.get()

            if address is None: # poison pill consumed
                input_queue.task_done()
                break

            try:
                lat, long = await geocoder.async_geocode(page, address)

                result = {
                    "address" : address,
                    "maps_url" : page.url,
                    "latitude" : lat,
                    "longitude" : long
                }

                print(f"{name} : {result}")
                
                await result_queue.put(result)

            except Exception as e:
                print(f"Failed to Extract URL {e}")

            finally:
                input_queue.task_done()
    finally:
        await context.close()
        print(f"[{name}] closed")
            