import logging
from logging import Logger 
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging():
    # Optional: configure root logging behavior
    logging.basicConfig(level=logging.INFO)

    # Force initialize a base logger (important for your system)
    get_logger("src")  # or __name__ of main modules


def get_logger(name: str):
    logger : Logger = logging.getLogger(name)

    if logger.handlers:
        return logger
    
    Path("logs").mkdir(exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=10_000_000,
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(
        formatter
    )

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )

    logger.addHandler(
        console_handler
    )

    logger.setLevel(
        logging.INFO
    )

    logger.propagate = False
 
    return logger