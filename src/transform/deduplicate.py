from logging import Logger
from pathlib import Path
import json
from src.config.npc_paths import DEDUPLICATED_SALE_LISTINGS, EXTRACTED_RENTAL_FILE, DEDUPLICATED_RENTAL_LISTINGS, EXTRACTED_SALE_FILE
from src.logger import get_logger

LOGGER : Logger = get_logger(__name__)

def deduplicate_properties(properties_path : Path) -> list[dict]:
    unique_properties : dict[str, dict] = {}
    with open(properties_path, "r", encoding="utf-8") as file_read:
        properties = json.load(file_read)
        
        for property in properties:
            link = property.get("link")
            
            if not link:
                continue
            
            unique_properties[link] = property
                
        return list(unique_properties.values())

def write_unique_properties(unique_properties : list[dict], output_path : Path):
    with open(output_path, "w", encoding="utf-8") as file_write:
        
        json.dump(unique_properties, file_write, indent=4, ensure_ascii=False)
            
    return len(unique_properties)


# For testing purposes, you can call the function with a sample path
if __name__ == "__main__":
    
    LOGGER.info(
        f"Starting deduplication process... | Input Path: {EXTRACTED_SALE_FILE}",
        extra={
            "event": "deduplication_started",
            "input_path": str(EXTRACTED_SALE_FILE),
        }
    )
    
    unique_props : list[dict] = deduplicate_properties(EXTRACTED_SALE_FILE)
    
    write_unique_properties(unique_props, DEDUPLICATED_SALE_LISTINGS)
    
    LOGGER.info(
        f"Deduplication process completed. | Unique properties: {len(unique_props)} | Output Path: {DEDUPLICATED_RENTAL_LISTINGS}",
        
        extra={
            "event": "deduplication_completed",
            "unique_count": len(unique_props),
            "output_path": str(DEDUPLICATED_SALE_LISTINGS),
        }
    )