from pathlib import Path
from asyncio import Queue
import json

async def write_address(
        result_queue : Queue, 
        output_path: Path
    ) -> None:

    if output_path.suffix != ".jsonl":
        raise ValueError(
            f"The file {output_path} is not a jsonl file"
        )
        
    with open(output_path, "a", encoding="utf-8") as file_append:
        
        while True:
            result = await result_queue.get()

            if result is None:
                result_queue.task_done()
                break
            
            file_append.write(json.dumps(result) + "\n")

            file_append.flush()

            result_queue.task_done()