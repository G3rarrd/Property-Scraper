import logging.config
import logging
from pathlib import Path

_LOGGING_INITIALIZED = False
def setup_logging() -> None:
    global _LOGGING_INITIALIZED
    if _LOGGING_INITIALIZED:
        return
    
    Path("logs").mkdir(exist_ok=True)
    
    config_dict = {
        "version" : 1,
        "formatters": {
            "default" : {
                "format": "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            },
        },
        
        "handlers":{
            "console" : {
                "class" : "logging.StreamHandler",
                "formatter": "default",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename":"logs/app.log",
                "maxBytes": 10_000_000,
                "backupCount": 5,
                "formatter":"default"
            },
        },
        
        "root" : {
            "level" : "WARNING",
            "handlers" : ["console"]  
        },
        
        "loggers": {
            "src": {
                "level" : "INFO",
                "handlers" : ["console", "file"],
                "propagate" : False,
            },
        }  
    }

    logging.config.dictConfig(config_dict)
    _LOGGING_INITIALIZED = True


setup_logging()