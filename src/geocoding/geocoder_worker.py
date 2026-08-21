# from asyncio import Queue
# # from geocoding.google_map_geocoder import GoogleMapsGeocoder
# from typing import List

# from src.fetchers.playwright.browser_manager import AsyncBrowserManager
# from .google_map_geocoder import GoogleMapsGeocoder


from src.fetchers.curl.curl import CurlFetcher
from asyncio import Queue

from src.geocoding.google_maps_geocoder import GoogleMapsGeocoder
from src.repositories.geocode_repository import get_coordinates, save_coordinates


async def worker(
    name: str, 
    geocoder : GoogleMapsGeocoder, 
    input_queue : Queue[str]
):
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
                
                    print( f"{name}. | Address: {cleaned_address} | Coordinates: ({lat},{lng})")
            else:
                print( f"{name}. | Address: {cleaned_address} | Coordinates: ({cached_res[0]},{cached_res[1]})")
                
        except Exception as e:
            print(f"Failed to save address coordinates: {e}")
            
        finally:
            input_queue.task_done()
                    

# async def worker(
#         name : str, 
#         browser_manager : AsyncBrowserManager, 
#         geocoder : GoogleMapsGeocoder, 
#         input_queue: Queue, 
#         result_queue : Queue,
#     ):
#     print(f"[{name}] Starting")

#     # Persistent Browser Context
#     block_resources : List[str] =c
#     context, page = await browser_manager.create_page(block_resources)
    
#     try:
#         while True:
#             address = await input_queue.get()

#             if address is None: # poison pill consumed
#                 input_queue.task_done()
#                 break

#             try:
#                 lat, long = await geocoder.async_geocode(page, address)

#                 result = {
#                     "address" : address,
#                     "maps_url" : page.url,
#                     "latitude" : lat,
#                     "longitude" : long
#                 }

#                 print(f"{name} : {result}")
                
#                 await result_queue.put(result)

#             except Exception as e:
#                 print(f"Failed to Extract URL {e}")

#             finally:
#                 input_queue.task_done()
#     finally:
#         await context.close()
#         print(f"[{name}] closed")
            