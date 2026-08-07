from pathlib import Path
import gzip
from playwright.async_api import Page, Response
from lxml import html
from typing import Optional
from src.config import settings
from src.logger import get_logger, Logger
from src.utils.url_parser import get_page_number
LOGGER : Logger = get_logger(__name__)

async def archive_html(page : Page, page_no : int, url : str, output_dir : str) -> Optional[Path]:
    for i in range(settings.network_retry_count):
        try:
            response : Optional[Response] = await page.goto(url, wait_until="domcontentloaded", timeout=300000)

            if response is None:
                return None
            
            html = await page.content()
            
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"page_{page_no}.html.gz"
            
            with gzip.open(output_path, 'wt', encoding='utf-8') as f:
                f.write(html)
            
            return output_path
        
        except Exception as e:
            LOGGER.error(
                f"Error archiving HTML for URL: {url} on attempt {i+1}/{settings.network_retry_count}. Error: {e}",
                extra={
                    "event": "html_archiving_error",
                    "url": url,
                    "attempt": i + 1,
                    "error": str(e),
                },
            )
            return None