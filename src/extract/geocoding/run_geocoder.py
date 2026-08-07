from pathlib import Path
from src.extract.geocoding.geo_cache_repo import GeoCacheRepository
from src.extract.geocoding.geocoder_worker import worker
from src.extract.geocoding.google_map_geocoder import GoogleMapsGeocoder
from src.extract.geocoding.address_loader import load_address
from src.extract.geocoding.address_writer import write_address
from src.extract.geocoding.google_maps_warmup import GoogleMapsWarmup
from asyncio import Queue
import asyncio
from scraper_infrastructre.browser_manager import AsyncBrowserManager

async def run_geocoder(
        cache_path : Path, 
        input_path : Path,
        num_workers : int,
        headless : bool=False
    ):
    # Load already stored data
    cache_repo : GeoCacheRepository = GeoCacheRepository(cache_path)
    
    # Geocoder Tool
    geocoder : GoogleMapsGeocoder = GoogleMapsGeocoder()
    
    # I want to convert these addresses to longitude and latitude
    # and skip the addresses that ive already converted
    addresses : set[str] = load_address(input_path, cache_repo)
    
    # Will be used by the workers
    input_queue : Queue = Queue()

    # Will be used to stream the data into the cache
    result_queue : Queue = Queue()

    for addr in addresses:
        await input_queue.put(addr)

    # Poison pills to stop the workers
    for _ in range(num_workers):
        await input_queue.put(None)

    # Browser instance 
    browser = AsyncBrowserManager("google_maps_geocoding_session.json", headless)
    await browser.start()

    # Deals with google consent page initially
    if not browser.session_file.exists():
        warmup = GoogleMapsWarmup(browser)
        await warmup.run()

    writer_task = asyncio.create_task(
        write_address(result_queue, cache_path)
    )
    
    workers = [
        asyncio.create_task(
            worker(
                f"Worker {i + 1}", browser, 
                geocoder, input_queue, result_queue)
            ) for i in range(num_workers)
    ]

    await writer_task

    await asyncio.gather(*workers)

    await browser.close()


