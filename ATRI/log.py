import sys
from pathlib import Path
from datetime import datetime

from nonebot.log import logger

from .config import BotSelfConfig


LOGGER_DIR = Path(".") / "data" / "logs"
LOGGER_DIR.mkdir(exist_ok=True, parents=True)

NOW_TIME = datetime.now().strftime("%Y%m%d-%H")

log_format = (
    "\033[36mATRI\033[0m "
    "| <g>{time:MM-DD HH:mm:ss}</g> "
    "| <lvl>{level}</lvl> "
    "<c><u>{name}</u></c> >> "
    "{message}"
)


class LoguruNameDealer:
    def __call__(self, record):
        log_handle = record["name"]
        if "nonebot.plugin.manager" in log_handle:
            plugin_name = log_handle.split(".")[-1]
            record["name"] = f"plugin.{plugin_name}"
        elif "nonebot_plugin_gocqhttp" in log_handle:
            plugin_name = log_handle.split("_")[-1]
            record["name"] = "gocqhttp"
        else:
            record["name"] = record["name"].split(".")[0]

        return record


logger.remove()
logger.add(
    sys.stdout,
    level="DEBUG" if BotSelfConfig.debug else "INFO",
    colorize=True,
    filter=LoguruNameDealer(),
    format=log_format,
)

logger.add(
    LOGGER_DIR / "info" / f"{NOW_TIME}.log",
    rotation="10 MB",
    enqueue=True,
    level="INFO",
    encoding="utf-8",
    format=log_format,
)

logger.add(
    LOGGER_DIR / "warning" / f"{NOW_TIME}.log",
    rotation="10 MB",
    enqueue=True,
    level="WARNING",
    encoding="utf-8",
    format=log_format,
)

logger.add(
    LOGGER_DIR / "error" / f"{NOW_TIME}.log",
    rotation="10 MB",
    enqueue=True,
    level="ERROR",
    encoding="utf-8",
    format=log_format,
)

logger.add(
    LOGGER_DIR / "debug" / f"{NOW_TIME}.log",
    rotation="10 MB",
    enqueue=True,
    level="DEBUG",
    encoding="utf-8",
    format=log_format,
)
