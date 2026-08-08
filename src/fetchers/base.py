from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class FetchResult:
    url: str
    status_code: int
    content: str

class Fetcher(ABC):

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass
    
    @abstractmethod
    async def get(self, url, **kwargs) -> FetchResult:
        pass