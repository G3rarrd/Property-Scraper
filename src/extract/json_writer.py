import json
from pathlib import Path

def write_to_json(output_file_path : Path, listings : list[dict]):
    with open(output_file_path, "w", encoding="utf-8") as fw:
        json.dump(listings, fw, indent=4, ensure_ascii=False)
        