import logging

from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR/"parrot.log"

def setup_logging():
    logging.basicConfig(
        level = logging.INFO,

        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),

        handlers = [
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(),
        ],
    )