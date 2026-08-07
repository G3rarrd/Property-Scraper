from .paths import DATA_DIR

ROOT = DATA_DIR / "nigeria_property_center"

RAW_RENTAL = ROOT / "rent" / "raw"
PROCESSED_RENTAL = ROOT / "rent" / "processed"

EXTRACTED_RENTAL_FILE = PROCESSED_RENTAL / "rental_listings.json"



DEDUPLICATED_RENTAL_LISTINGS = PROCESSED_RENTAL / "rental_listings_dedup.json"
CLEANED_RENTAL_LISTINGS = ROOT / "rent" / "rental_listings_cleaned.json"