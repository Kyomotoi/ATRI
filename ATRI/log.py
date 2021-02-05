from pathlib import Path
from datetime import datetime

from nonebot.log import logger, default_format


LOGGER_DIR = Path('.') / 'ATRI' / 'data' / 'logs'
LOGGER_DIR.parent.mkdir(exist_ok=True, parents=True)

NOW_TIME = datetime.now().strftime('%Y%m%d-%H%M%S')

logger.add(
    LOGGER_DIR / 'info' / f"{NOW_TIME}-INFO.log",
    rotation="10 MB",
    enqueue=True,
    level="INFO",
    encoding="utf-8",
    format=default_format
)

logger.add(
    LOGGER_DIR / 'warning' / f"{NOW_TIME}-WARNING.log",
    rotation="10 MB",
    enqueue=True,
    level="WARNING",
    encoding="utf-8",
    format=default_format
)

logger.add(
    LOGGER_DIR / 'error' / f"{NOW_TIME}-ERROR.log",
    rotation="10 MB",
    enqueue=True,
    level="ERROR",
    encoding="utf-8",
    format=default_format
)

logger.add(
    LOGGER_DIR / 'debug' / f"{NOW_TIME}-DEBUG.log",
    rotation="10 MB",
    enqueue=True,
    level="DEBUG",
    encoding="utf-8",
    format=default_format
)
