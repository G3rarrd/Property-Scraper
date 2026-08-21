from src.fetchers.curl.curl import CurlFetcher
from asyncio import Queue

from src.geocoding.google_maps_geocoder import GoogleMapsGeocoder
from src.repositories.geocode_repository import get_coordinates, save_coordinates
import logging

import os
from dotenv import load_dotenv

load_dotenv()



LOGGER = logging.getLogger(__name__)

async def worker(
    name: str, 
    geocoder : GoogleMapsGeocoder, 
    input_queue : Queue[str]
):
    db_name = os.getenv("DATABASE_NAME", "default")
    while True:
        address = await input_queue.get()
        
        if address == None:
            input_queue.task_done()
            break
        
        try:
            cleaned_address = geocoder.normalize_address(address)
            address_key = geocoder.make_key(cleaned_address)
            cached_res = get_coordinates(address_key)
            
            if not cached_res or not cached_res[0]:
                lat, lng = await geocoder.geocode(cleaned_address)
                if lat and lng:
                    save_coordinates(address_key, cleaned_address, lat, lng)
                    LOGGER.info(
                        "[%s] Saved coordinates | address='%s' coords=(%.6f, %.6f) db='%s'",
                        name, cleaned_address, lat, lng, db_name
                    )
                else:
                    LOGGER.warning(
                        "[%s] Geocoding returned no result | address='%s'",
                        name, cleaned_address
                    )
            else:
                LOGGER.info("Address : %s already exists", cleaned_address)
                
        except Exception as e:
            LOGGER.exception("[%s] Failed to process address='%s' | Error=%s", name, address, e)
            
        finally:
            input_queue.task_done()
                    