from pathlib import Path
import asyncio

from src.extract.nigeria_property_center.pipeline import pipeline

async def main_async():
    await pipeline()

if "__main__" == __name__:
    asyncio.run(main_async())