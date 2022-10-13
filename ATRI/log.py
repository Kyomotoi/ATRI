import sys
from pathlib import Path
from datetime import datetime

from nonebot.log import logger as log

from ATRI import conf


LOGGER_DIR = Path(".") / "data" / "logs"
LOGGER_DIR.mkdir(exist_ok=True, parents=True)

_NOW_TIME = datetime.now().strftime("%Y%m%d-%H")

_LOG_FORMAT = (
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


log.remove()
log.add(
    sys.stdout,
    level="DEBUG" if conf.BotConfig.debug else "INFO",
    colorize=True,
    filter=LoguruNameDealer(),
    format=_LOG_FORMAT,
)

log.add(
    LOGGER_DIR / "info" / f"{_NOW_TIME}.log",
    rotation="10 MB",
    enqueue=True,
    level="INFO",
    encoding="utf-8",
    format=_LOG_FORMAT,
)

log.add(
    LOGGER_DIR / "warning" / f"{_NOW_TIME}.log",
    rotation="10 MB",
    enqueue=True,
    level="WARNING",
    encoding="utf-8",
    format=_LOG_FORMAT,
)

log.add(
    LOGGER_DIR / "error" / f"{_NOW_TIME}.log",
    rotation="10 MB",
    enqueue=True,
    level="ERROR",
    encoding="utf-8",
    format=_LOG_FORMAT,
)

log.add(
    LOGGER_DIR / "debug" / f"{_NOW_TIME}.log",
    rotation="10 MB",
    enqueue=True,
    level="DEBUG",
    encoding="utf-8",
    format=_LOG_FORMAT,
)
