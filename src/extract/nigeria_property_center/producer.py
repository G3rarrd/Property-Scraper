from asyncio import Queue

async def producer(url : str, input_queue : Queue, start : int, end : int):
    for i in range(start, end + 1):
        page_url = f"{url}?page={i}&sort=2"
        await input_queue.put(page_url)