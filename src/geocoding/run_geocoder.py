import asyncio
import json
from src.db.connection import get_connection
from src.fetchers.curl.curl import CurlFetcher
from src.geocoding.geocoder_worker import worker
from src.geocoding.google_maps_cookies import GoogleMapsCookieManger
from lxml import html

import os
import psycopg
from dotenv import load_dotenv

from src.geocoding.google_maps_geocoder import GoogleMapsGeocoder
from src.repositories.geocode_repository import get_coordinates, save_coordinates

load_dotenv()


async def run():
    # get sorted addresses
    with open("data/nigeria_property_center/rent/processed/rental_listings.json", "r", encoding="utf-8") as f:
        listings = json.load(f)
    addresses = sorted(list(set(listing.get("address", "") for listing in listings)))
    print(f"{len(addresses)} unique addresses found")
    
    # Handle cookies
    filename : str = "gmap_cookies"
    cookie_manager = GoogleMapsCookieManger(filename)
    
    if not cookie_manager.filepath.exists():
        await cookie_manager.solve_google_maps_cookies()
        cookie_manager.save_cookies()

    # Handle Requests
    curl = CurlFetcher()
    await curl.start()
    curl.session.cookies = cookie_manager.get_cookies()
    
    # Geocoder
    geocoder = GoogleMapsGeocoder(curl)
    
    worker_count = 1
    input_queue = asyncio.Queue()
    
    for address in addresses:
        await input_queue.put(address)
        
    for _ in range(worker_count):
        await input_queue.put(None)
        
    workers = [asyncio.create_task(
        worker(f"Worker_{i+1}", geocoder, input_queue)) 
               for i in range(worker_count)]
    
    await input_queue.join()
    await asyncio.gather(*workers)
    
if "__main__" == __name__:
    asyncio.run(run())