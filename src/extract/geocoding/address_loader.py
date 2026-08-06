from .geo_cache_repo import GeoCacheRepository
from pathlib import Path
import json

def load_address(
        properties_jsonl: Path, 
        cache_repo : GeoCacheRepository
    )-> set[str]:

    if properties_jsonl.suffix != ".jsonl":
        raise ValueError(f"The file {properties_jsonl} is not a jsonl file")
    
    # load the addresses that have been converted and assiged 
    # to jsonl file already

    cache_repo.load()

    addresses : set[str] = set()

    with open(properties_jsonl, "r", encoding="utf-8") as file_read:
        
        for line in file_read:
            if not line.strip():
                continue

            record = json.loads(line)

            address = record.get("address", "")

            if not address:
                continue

            if cache_repo.exists(address):
                continue

            addresses.add(address)

    return addresses