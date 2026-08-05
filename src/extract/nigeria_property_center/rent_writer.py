from asyncio import Queue
from pathlib import Path
import json

from logger import get_logger, Logger
LOGGER : Logger = get_logger(__name__)

async def npc_writer(result_queue : Queue, output_file_path : Path) :
    LOGGER.info(
        "writer_started",
        extra={
            "event": "writer_started",
            "output_path": str(output_file_path),
        },
    )

    write_count = 0

    with open(output_file_path, "a", encoding="utf-8") as file_append:
        while True:
        
            property = await result_queue.get()

            if property is None:
                LOGGER.info(
                    "writer_stopping",
                    extra={
                        "event": "writer_stopping",
                        "write_count": write_count,
                    },
                )

                result_queue.task_done()
                break

            try:
                file_append.write(json.dumps(property) + "\n")
                file_append.flush()

                write_count += 1

            except Exception as e:

                LOGGER.exception(
                    "write_failed",
                    extra={
                        "event": "write_failed",
                        "error_type": type(e).__name__,
                        "error_message": str(e),
                    },
                )

            finally:
                result_queue.task_done()

    LOGGER.info(
        "writer_closed",
        extra={
            "event": "writer_closed",
            "total_written": write_count,
        },
    )