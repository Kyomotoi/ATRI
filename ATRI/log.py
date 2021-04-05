import sys
from pathlib import Path
from datetime import datetime

from nonebot.log import logger, default_format

from .config import Config


LOGGER_DIR = Path('.') / 'ATRI' / 'data' / 'logs'
LOGGER_DIR.parent.mkdir(exist_ok=True, parents=True)

NOW_TIME = datetime.now().strftime('%Y%m%d-%H')

log_format = (
    "\033[36mATRI\033[0m "
    "| <g>{time:MM-DD HH:mm:ss}</g> "
    "| <lvl>{level}</lvl> "
    "<c><u>{name}</u></c> >> "
    "{message}"
)


logger.remove()
logger.add(
    sys.stdout,
    level="DEBUG" if Config.BotSelfConfig.debug else "INFO",
    colorize=True,
    format=log_format
)

logger.add(
    LOGGER_DIR / "info" / f"{NOW_TIME}-INFO.log",
    rotation="10 MB",
    enqueue=True,
    level="INFO",
    encoding="utf-8",
    format=log_format
)

logger.add(
    LOGGER_DIR / 'warning' / f"{NOW_TIME}-WARNING.log",
    rotation="10 MB",
    enqueue=True,
    level="WARNING",
    encoding="utf-8",
    format=log_format
)

logger.add(
    LOGGER_DIR / 'error' / f"{NOW_TIME}-ERROR.log",
    rotation="10 MB",
    enqueue=True,
    level="ERROR",
    encoding="utf-8",
    format=log_format
)

logger.add(
    LOGGER_DIR / 'debug' / f"{NOW_TIME}-DEBUG.log",
    rotation="10 MB",
    enqueue=True,
    level="DEBUG",
    encoding="utf-8",
    format=log_format
)
