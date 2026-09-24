import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "data"
LOG_FILE = LOG_DIR / "concerthub.log"


def setup_logging():
    """Configure application logging and return the ConcertHub logger."""
    LOG_DIR.mkdir(exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    return logging.getLogger("ConcertHub")
