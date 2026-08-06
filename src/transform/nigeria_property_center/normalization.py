from typing import Optional
import re
from config.npc_paths import DEDUPLICATED_RENTAL_LISTINGS

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
    if period_str is None:
        return None

    period_str = period_str.lower()
    if "month" in period_str:
        return "monthly"
    elif "year" in period_str:
        return "yearly"
    else:
        return None
    

