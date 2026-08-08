from src.fetchers.base import FetchResult, Fetcher
from random import choice
from curl_cffi.requests import AsyncSession
import asyncio

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
            
    async def get(self, url, **kwargs) -> FetchResult:
        if not self.session:
            raise("Session has Not Started!")
        
        response = await self.session.get(url, **kwargs)
        
        
        response.raise_for_status()
        
        return FetchResult(
            url=str(response.url),
            status_code=response.status_code,
            content=response.text
        )

async def demo():
    curl = CurlFetcher()
    await curl.start()
    print(curl.impersonate)
    response = await curl.get("https://nigeriapropertycentre.com/for-rent/?q=for-rent&sort=2")
    print(response.content)
    
        
            
if __name__ == "__main__":
    asyncio.run(demo())
