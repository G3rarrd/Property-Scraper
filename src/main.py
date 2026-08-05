from pathlib import Path
# from src.storage.storage_manager import StorageManager
# from src.scraper.rent_scrape import scrape
# from src.geocoding.address_loader import load_address
# from src.geocoding.address_writer import write_address
# from src.geocoding.geo_cache_repo import GeoCacheRepository
# from src.geocoding.google_map_geocoder import GoogleMapsGeocoder
# from src.infrastructre.async_browser_manager import AsyncBrowserManager


# from asyncio import Queue
import asyncio

from extract.nigeria_property_center.pipeline import pipeline
# from playwright.async_api import async_playwright, Browser
# from src.geocoding.geocoder_worker import worker
# from src.geocoding.google_maps_warmup import GoogleMapsWarmup
# from extract.npc_rent_scraper import run_scraper
# from geocoding.run_geocoder import run_geocoder
# from logger import setup_logging

async def main_async():
    await pipeline()
    # setup_logging()

    # parent_path : Path = Path("../storage")
    # rental_raw_data_path : Path = parent_path / "rental_properties_raw.jsonl"
    # cache_path : Path = parent_path / "address_coordinates_async.jsonl"
    # await run_geocoder(cache_path, rental_raw_data_path, 3, False)

    # await run_scraper(output_path, 900, 2000, 5)

    # properties_file : Path = parent_path / "properties_dedup.jsonl"
    # geocode_file_name : str = "address_coordinates_async.jsonl"
    
    # geocoded_data_path : Path = parent_path / geocode_file_name

    # cache_repo : GeoCacheRepository = GeoCacheRepository(geocoded_data_path)
    
    # geocoder : GoogleMapsGeocoder = GoogleMapsGeocoder()

    # addresses : set[str] = load_address(properties_file, cache_repo)

    # print(f"{len(addresses)} unique addresses collected")
    
    # address_queue : Queue = Queue()

    # num_workers : int = 3

    # # Add addresses to asyncio.Queue
    # for address in addresses:
    #     await address_queue.put(address)

    # # Add poison pills to stop workers
    # for _ in range(num_workers):
    #     await address_queue.put(None)

    # # Initiate browser state
    # browser = AsyncBrowserManager(
    #     "google_maps_geocoding_session.json", 
    #     headless=True
    # )

    # # starts browser
    # await browser.start() 

    # # Dummy browser to save initial cookies
    # if not browser.session_file.exists():
    #     warmup = GoogleMapsWarmup(browser)
    #     await warmup.run()


    # result_queue : Queue = Queue()

    # writer_task = asyncio.create_task(
    #     write_address(result_queue, geocoded_data_path)
    # )

    # # Workers
    # workers = [
    #     asyncio.create_task(
    #         worker(f"Worker {i + 1}", browser, geocoder, address_queue, result_queue)
    #     )
    #     for i in range(num_workers)
    # ]
    
    # await writer_task

    # await asyncio.gather(*workers)

    # await browser.close()
    
    # print(f"\nTota scraped: {len(result_queue)}")


if "__main__" == __name__:
    asyncio.run(main_async())