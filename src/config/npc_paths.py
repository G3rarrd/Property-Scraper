from .paths import DATA_DIR

ROOT = DATA_DIR / "nigeria_property_center"

RAW_RENTAL_LISTINGS = ROOT / "rent" / "rental_listings.jsonl"
DEDUPLICATED_RENTAL_LISTINGS = ROOT / "rent" / "rental_listings_deduplicated.json"
CLEANED_RENTAL_LISTINGS = ROOT / "rent" / "rental_listings_cleaned.json"