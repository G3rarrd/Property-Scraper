from pathlib import Path
import gzip
from typing import Optional

class HTMLLoader:
    def load(self, raw_html_path: Path):
        html_path = Path(raw_html_path)
        
        if html_path.suffix != ".gz":
            return None
        
        with gzip.open(html_path, "rt", encoding="utf-8") as f:
            return f.read()
        
        return html_path.read_text(encoding="utf-8")
        
        