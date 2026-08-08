from asyncio import Queue
from pathlib import Path
import json
from dataclasses import asdict
from lxml import html
from typing import Optional
from tqdm import tqdm

from src.config.npc_paths import EXTRACTED_RENTAL_FILE, EXTRACTED_SALE_FILE, RAW_RENTAL, PROCESSED_RENTAL, RAW_SALE
from src.extract.json_writer import write_to_json
from src.extract.nigeria_property_center.rent_parser import extract_property_cards, parse_property
from src.storage.html_loader import HTMLLoader
from .rent_model import RentField
from src.logger import get_logger, Logger
LOGGER : Logger = get_logger(__name__)



def rent_writer(loader : HTMLLoader, data_dir : Path) :
    html_data = list(data_dir.glob("*.html.gz"))
    
    extract_html_bar = tqdm(total=len(html_data))
    
    properties : list[dict] = []
    for file in html_data:
        html_text : Optional[str] = loader.load(file)

        if not html_text:
            continue
        
        tree = html.fromstring(html_text)
        
        property_cards = extract_property_cards(tree)
        
        for prop_card in property_cards:
            prop_info : Optional[RentField] = parse_property(prop_card)
            
            if not prop_info:
                continue
            
            properties.append(asdict(prop_info))
            
        extract_html_bar.update(1)
        extract_html_bar.set_postfix(properties_found=f"{len(properties)}")
    
    
    extract_html_bar.close()
    
    return properties

    
    
if __name__ == "__main__":
    extracted_file_path = EXTRACTED_SALE_FILE
    # extracted_file_path.mkdir(parents=True, exist_ok=True)

    loader = HTMLLoader()
    
    properties = rent_writer(loader, RAW_SALE)
    
    write_to_json(extracted_file_path, properties)
    