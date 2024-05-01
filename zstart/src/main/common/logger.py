import logging, logging.config
from pathlib import Path

logger = logging.getLogger("ZStart")

def initLogger():
    f = Path("resources/config/stdout.json")
    logging.config.fileConfig(f)
    logging.basicConfig(level="INFO")