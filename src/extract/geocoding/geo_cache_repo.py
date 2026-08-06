from pathlib import Path
import json

class GeoCacheRepository:
    def __init__(self, cache_path: Path):
        if cache_path.suffix != ".jsonl":
            raise ValueError(f"The file {cache_path} must be a jsonl file")
        
        self.__cache_path = cache_path
        self.geo_cache :dict[str, tuple[float, float]] = {}
        self.load()

    def load(self):
        if not self.__cache_path.exists():
            return
        
        with open(self.__cache_path, "r", encoding="utf-8") as file_read:
            for line in file_read:
                if line.strip():
                    record = json.loads(line)
                    address : str = record["address"]
                    latitude : str = record["latitude"]
                    longitude : str = record["longitude"]
                    self.geo_cache[address] = (float(latitude), float(longitude))

    def append(self, record: dict) -> None:
        address = record["address"]

        lat = float(record["latitude"])
        lng = float(record["longitude"])

        self.geo_cache[address] = (lat, lng)
        with open(self.__cache_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def get(self, address : str) -> tuple[float, float]:
        return self.geo_cache.get(address)
    
    def exists(self, address : str) -> bool:
        return address in self.geo_cache