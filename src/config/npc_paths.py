from .paths import DATA_DIR

ROOT = DATA_DIR / "nigeria_property_center"

RENTAL = ROOT / "rent" 
SALE = ROOT / "for-sale"
SALE.mkdir(parents=True, exist_ok=True)
RENTAL.mkdir(parents=True, exist_ok=True)

RAW_RENTAL = RENTAL / "raw"
RAW_SALE = SALE / "raw" 

PROCESSED_RENTAL = RENTAL / "processed"
PROCESSED_SALE = SALE / "processed"

EXTRACTED_RENTAL_FILE = PROCESSED_RENTAL / "for_rent_listings.json"
EXTRACTED_SALE_FILE = PROCESSED_SALE / "for_sale_listings.json"

DEDUPLICATED_RENTAL_LISTINGS = PROCESSED_RENTAL / "for_rent_listings_dedup.json"
DEDUPLICATED_SALE_LISTINGS = PROCESSED_SALE / "for_sale_listings_dedup.json"

CLEANED_RENTAL_LISTINGS =  PROCESSED_RENTAL / "for_rent_listings_cleaned.json"