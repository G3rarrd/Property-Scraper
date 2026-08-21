import asyncio
import json
from src.fetchers.curl.curl import CurlFetcher
from src.geocoding.geocoder_worker import worker
from src.geocoding.google_maps_cookies import GoogleMapsCookieManger
from lxml import html

import os
import psycopg
from dotenv import load_dotenv

from src.geocoding.google_maps_geocoder import GoogleMapsGeocoder
import logging

from src.logger import setup_logging

load_dotenv()
logger = logging.getLogger(__name__)

async def run():
    logger.info("Starting geocoding pipeline...")
    # Load and deduplicate addresses
    data_path = "data/nigeria_property_center/rent/processed/rental_listings.json"
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            listings = json.load(f)
        addresses = sorted(list(set(listing.get("address", "") for listing in listings if listing.get("address"))))
        logger.info("Loaded %d unique addresses from %s", len(addresses), data_path)
    except Exception:
        logger.exception("Failed to load listings from %s", data_path)
        return
    
    # Handle cookies
    cookie_manager = GoogleMapsCookieManger("gmap_cookies")
    if not cookie_manager.filepath.exists():
        await cookie_manager.solve_google_maps_cookies()
        cookie_manager.save_cookies()
    else:
        logger.info("Loaded cached Google Maps cookies from %s", cookie_manager.filepath)

    # Handle Requests
    curl = CurlFetcher()
    await curl.start()
    curl.session.cookies = cookie_manager.get_cookies()
    
    try:
        # Geocoder & Queue Setup
        geocoder = GoogleMapsGeocoder(curl)
        worker_count = 1
        input_queue = asyncio.Queue()
        
        for address in addresses:
            await input_queue.put(address)
        
        # poison pills to shutdown workers   
        for _ in range(worker_count):
            await input_queue.put(None)
        
        logger.info("Spawning %d worker(s) for %d tasks...", worker_count, len(addresses))
        workers = [asyncio.create_task(
            worker(f"Worker_{i+1}", geocoder, input_queue)) 
                for i in range(worker_count)]
        
        await input_queue.join()
        await asyncio.gather(*workers)
        logger.info("Geocoding pipeline completed successfully.")
    except Exception:
        logger.exception("Uncaught exception during geocoding pipeline execution")
    finally:
        logger.info("Closing HTTP fetcher session...")
        await curl.close()
    
if "__main__" == __name__:
    setup_logging()
    asyncio.run(run())