from pathlib import Path
import json
from typing import Any

from processing.normalization import *


class StorageManager:
    def __init__(self, logger, file_path: str | Path):
        self.logger = logger
        self.file_path = Path(file_path)

    def append_jsonl(self, results: list[dict[str, Any]]) -> None:
        with open(self.file_path, "a", encoding="utf-8") as f:
            for item in results:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    def remove_duplicates_jsonl(self, output_path: str | Path, key: str = "link") -> Path:

        output_path = Path(output_path)
        seen: set[Any] = set()

        with open(self.file_path, "r", encoding="utf-8") as file_in, \
             open(output_path, "w", encoding="utf-8") as fout:

            for line in file_in:
                line = line.strip()
                if not line:
                    continue

                data = json.loads(line)
                value = data.get(key)

                if value in seen:
                    continue

                seen.add(value)

                fout.write(json.dumps(data, ensure_ascii=False) + "\n")

        self.logger.info(f"Deduped: {len(seen)} unique items")
        return output_path

    def jsonl_to_json(self, output_path: str | Path,input_path: str | Path | None = None) -> Path:

        input_path = Path(input_path or self.file_path)
        output_path = Path(output_path)

        data = []

        with open(input_path, "r", encoding="utf-8") as file_in:
            for line in file_in:
                line = line.strip()
                if line:
                    data.append(json.loads(line))

        with open(output_path, "w", encoding="utf-8") as fout:
            json.dump(data, fout, ensure_ascii=False, indent=2)

        self.logger.info(f"Converted to JSON: {len(data)} items")
        return output_path
    
    def transform_jsonl_to_json(self, output_path: str | Path,input_path: str | Path | None = None) -> Path:

        input_path = Path(input_path or self.file_path)
        output_path = Path(output_path)

        cleaned_data = []

        with open(input_path, "r", encoding="utf-8") as file_in:
            for line in file_in:
                if not line.strip():
                    continue

                record = json.loads(line)

                cleaned_record = {
                    "name": record.get("name"),
                    "listing_type" : record.get("listing_type"),
                    "title" : record.get("title"),
                    "description" : record.get("description"),
                    "thumbnail" : record.get("thumbnail"),
                    "address": clean_address(record.get("address", "")),
                    "price": clean_price(record.get("price_info", [])),
                    "features": clean_feature(record.get("features_info", [])),
                    "marketer": clean_marketer(record.get("marketer_info", [])),
                    "link": record.get("link"),
                }

                cleaned_data.append(cleaned_record)

        with open(output_path, "w", encoding="utf-8") as file_out:
            json.dump(cleaned_data, file_out, ensure_ascii=False, indent=2)

        self.logger.info(f"Converted to Transformed JSON: {len(cleaned_data)} items")
        return output_path