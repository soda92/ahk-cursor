from pathlib import Path
import logging
import logging.handlers

CURRENT = Path(__file__).resolve().parent
log_file = CURRENT.parent.joinpath("soda-ahk.cursor.log")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(
    logging.handlers.RotatingFileHandler(
        log_file,
        mode="a",
        maxBytes=1024 * 1024 * 10,
        backupCount=5,
        encoding="utf8",
        delay=True,
        errors=None,
    )
)
