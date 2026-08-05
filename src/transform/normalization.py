from typing import Optional
import re

class PropertyDataCleanerUtils:
    """ 
    Transforms the individual raw dict data scraped and stored
    in the jsonl file.
    """
    @staticmethod
    def clean_marketer(marketer_info : list[str]) -> dict:

        marketer_dict : dict = {
            "agent_name" : None, 
            "agent_phone_number" : None
        }
        
        if not marketer_info:
            return marketer_dict
        
        if len(marketer_info) == 2:
            marketer_dict["agent_name"] = marketer_info[0]
            marketer_dict["agent_phone_number"] = marketer_info[1]
            return marketer_dict
        

        marketer_dict["agent_phone_number"] = marketer_info[0]

        return marketer_dict

    @staticmethod
    def clean_feature(features_info : list[str]) -> dict:
        # the unique ammenities are gotten from the results of the exploratory 
        # data analysis done in notebooks/npc_rent_data_eda.ipynb
        FEATURE_MAP = {
            "Bedroom": "bedroom",
            "Bedrooms": "bedroom",
            "Bathroom": "bathroom",
            "Bathrooms": "bathroom",
            "Toilet": "toilet",
            "Toilets": "toilet",
            "Parking Space": "parking_space",
            "Parking Spaces": "parking_space",
            "sqm Covered Area": "covered_area_sqm",
            "sqm Total Area": "total_area_sqm",
        }

        feature_dict : dict = {
            "bedroom": None,
            "bathroom": None,
            "toilet": None,
            "parking_space": None,
            "covered_area_sqm": None,
            "total_area_sqm": None,
        }

        for feature in features_info:
            # splits the leading number from the ammenity
            match = re.match(r"(-?[\d,]+)\s+(.+)", feature.strip())

            if not match:
                continue

            value = int(match.group(1).replace(",", "")) # converting leading number to integer for better interpretation
            label = match.group(2) # the ammenity

            key = FEATURE_MAP.get(label) 

            if key:
                feature_dict[key] = None if value < 0 else value

        return feature_dict

    @staticmethod
    def clean_price(price_info: list[str]) -> dict:

        def extract_number(text: str) -> Optional[int]:
            numbers = re.sub(r"[^\d]", "", text)
            return int(numbers) if numbers else None
        
        price_dict : dict = {
            "currency":None,
            "amount": None,
            "period":None,
            "area_unit":None,
            "original_currency": None,
            "original_amount": None,
        }

        currency_dict : dict[str, str]= {
            "₦" : "NGN",
            "$" : "USD"
        }

        # price infos of length 1 usually mean the info is a "Call for Price" text
        if not price_info or len(price_info) == 1:
            return price_dict
        
        currency_symbol : str = price_info[0]
        amount : Optional[int] = extract_number(price_info[1])
        other_data : str = " ".join(price_info[2:]).lower()

        price_dict["currency"] = currency_dict[currency_symbol]
        price_dict["amount"] = amount


        # Approximate naira value
        if "approx" in other_data:
            # means the initial number found was in a currency other than dollars
            price_dict["original_amount"] = price_dict["amount"]
            price_dict["original_currency"] = price_dict["currency"]

            # Get the naira value
            price_dict["currency"] = "NGN"
            price_dict["amount"] = extract_number(other_data)
    
        # Period
        if "per annum" in other_data:
            price_dict["period"] = "year"
        elif "per month" in other_data:
            price_dict["period"] = "month"
        elif "per day" in other_data:
            price_dict["period"] = "day"
        elif "per hour" in other_data:
            price_dict["period"] = "hour"

        # Area unit
        if "square meter" in other_data:
            price_dict["area_unit"] = "sqm"
        elif "square foot" in other_data:
            price_dict["area_unit"] = "sqft"

        return price_dict

    @staticmethod
    def clean_address(address: str) -> dict:
        address_dict = {
            "full_address": address,
            "state": None,
            "locality": None,
            "latitude" : None,
            "longitude" : None
        }

        if not address:
            return address_dict

        parts = [part.strip() for part in address.split(",") if part.strip()]

        if len(parts) >= 1:
            address_dict["state"] = parts[-1]

        if len(parts) >= 2:
            address_dict["locality"] = parts[-2]


        return address_dict