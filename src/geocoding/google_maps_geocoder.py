from collections import Counter
import re
import hashlib
from src.fetchers.curl.curl import CurlFetcher
from lxml import html
import json
import asyncio

class GoogleMapsGeocoder:
    def __init__(self, curl : CurlFetcher, retry_count : int=10):
        self.curl = curl
        self.retry_count = retry_count
        
    def _build_search(self, address : str) -> str:
        parsed_address = address.replace(" ", "+")
        return f"https://www.google.com/maps/search/{parsed_address}"
    
    def find_coordinates(self, node):

        if isinstance(node, list):
            if (
                len(node) == 4
                and node[0] is None and node[1] is None
                and isinstance(node[2], (int, float))
                and isinstance(node[3], (int, float))
                and -90 <= node[2] <= 90
                and -180 <= node[3] <= 180
            ):
                return (node[2], node[3])
            for item in node:
                found = self.find_coordinates(item)
                if found:
                    return found
        elif isinstance(node, dict):
            for v in node.values():
                found = self.find_coordinates(v)
                if found:
                    return found
        return None

    
    async def _get_raw_coordinates_data(self, address_url : str):
        for i in range(self.retry_count):
            try:
                response = await self.curl.get_response(address_url)
                
                html_content = response.text
                tree = html.fromstring(html_content)
                search_link = tree.xpath("//link/@href")[0]
                coordinates_url = "https://www.google.com" + search_link.replace("&amp;", "&")
                
                response = await self.curl.get_response(coordinates_url)
                raw_response = response.text.lstrip(")]}'\n") # returns a json list
                
                return json.loads(raw_response)
            
            except Exception as e:
                print(f"Error: {e} | Retries made: [{i + 1}/{self.retry_count}]")
                await asyncio.sleep(5)
                
    def normalize_address(self, address : str):
        text = address.strip().strip(",").strip()
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\s*,\s*", ", ", text)
        text = re.sub(r"@\s*", "", text).strip()
        return text
    
    def make_key(self, address: str) -> str:
        normalized = address.strip().lower()
        return hashlib.sha256(normalized.encode()).hexdigest()
        
    async def geocode(self, address : str) -> tuple[str, float | None, float | None]:
        address_url = self._build_search(address)
        data = await self._get_raw_coordinates_data(address_url)
        coords = self.find_coordinates(data)
        if not coords:
            return None, None
        (lat, lng) = coords
        return lat, lng
        
        