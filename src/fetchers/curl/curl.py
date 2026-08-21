from src.fetchers.base import FetchResult, Fetcher
from random import choice
from curl_cffi.requests import AsyncSession, Response
import asyncio
from urllib.parse import quote
BROWSERS = ["chrome", "firefox", "safari"]

class CurlFetcher(Fetcher):
    def __init__(self,):
        self.session : AsyncSession | None = None
        self.impersonate : str | None = None
        
    async def start(self):
        if self.session:
            print("Session is Already Active")
            return 
        
        self.impersonate = choice(BROWSERS)
        
        self.session = AsyncSession(
            impersonate=self.impersonate,   
        )
        
    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None
            
    async def get_response(self, url, **kwargs) -> Response:
        if not self.session:
            raise("Session has Not Started!")
        
        response : Response = await self.session.get(url, **kwargs)
        response.raise_for_status()
        return response
            
    async def get(self, url, **kwargs) -> FetchResult:
        response = self.get_response(url, **kwargs)
        
        return FetchResult(
            url=str(response.url),
            status_code=response.status_code,
            content=response.text
        )

async def demo():
    # cookies = await get_google_maps_cookies()
    # print(cookies)
    
    # curl = CurlFetcher()
    # await curl.start()
    
    # url = ("https://www.google.com/maps/search/"
    #              f"?api=1&query={quote("Periwinkle Lifestyle Estate, Ikate, Lekki, Lagos")}")
    
    # for cookie in cookies:
    #     curl.session.cookies.set(
    #         cookie["name"],
    #         cookie["value"],
    #         domain=cookie["domain"],
    #         path=cookie["path"],
    #     )
        
    # response = await curl.get_response(url)
    # print("Final URL:", response.url)
    # print("Status:", response.status_code)
    # await curl.close()
    pass    
            
if __name__ == "__main__":
    asyncio.run(demo())
