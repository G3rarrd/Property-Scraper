from typing import Optional
import re
from src.config.npc_paths import DEDUPLICATED_RENTAL_LISTINGS

def normalize_price(price_str: Optional[str]) -> dict[str]:
    price_dict = {"currency": None, "price": None}
    if price_str is None:
        return None

    try:
        price_dict["currency"] = price_str[0] if price_str else None
        price_dict["price"] = re.sub(r'[^\d.]', '', price_str) if price_str else None
        return price_dict
    
    except ValueError:
        return None
    
def normalize_period(period_str: Optional[str]) -> str:
    period_dict = {"/hr" : "hourly", "/yr" : "yearly", "/mo" : "monthly", "/day" : "daily"}
    if period_str is None or period_str not in period_dict:
        return None

    period_str = period_str.lower()

    return period_dict[period_str]
    

def normalize_features(features : list[str]) -> str:
    FEATURE_MAP = {
        "Beds": "bedroom",
        "Baths": "bathroom",
        "Toilets": "toilet",
        "Parking": "parking_space",
        "sqm": "total_area_sqm",
    }
    
    features_dict= {
        "bedroom" : None,
        "bathroom" : None,
        "toilet" : None,
        "parking_space" : None,
        "total_area_sqm" : None
    }
    
    for feature in features:
        split_feat : list[str] = feature.split(" ")
        quantity : int = int(split_feat[0])
        ammenity : str = split_feat[1]
        mapped : str = FEATURE_MAP[ammenity]
        
        features_dict[mapped] = quantity
        
    return features_dict