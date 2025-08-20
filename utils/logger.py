import logging
import logging.config
import os

LOG_CONFIG = os.path.join(os.path.dirname(__file__), "..", "config", "logging.ini")

def get_logger(name: str = None) -> logging.Logger:
    logging.config.fileConfig(LOG_CONFIG, disable_existing_loggers=False)
    return logging.getLogger(name if name else __name__)
