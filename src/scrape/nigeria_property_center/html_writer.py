from pathlib import Path
import gzip
from playwright.async_api import Page, Response
from lxml import html
from typing import Optional
from src.config import settings
from src.logger import get_logger, Logger
from src.utils.url_parser import get_page_number
LOGGER : Logger = get_logger(__name__)

async def archive_html(content : str,  page_no : int, output_dir : str) -> Optional[Path]:
    output_path : str = ""
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"page_{page_no}.html.gz"
        
        with gzip.open(output_path, 'wt', encoding='utf-8') as f:
            f.write(content)
        
        return output_path
    
    except Exception as e:
        print(e)
        return None