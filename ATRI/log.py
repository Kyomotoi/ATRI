from pathlib import Path
from datetime import datetime
from nonebot.log import logger, default_format

LOGGER_INFO_PATH = Path(
    '.'
) / 'ATRI' / 'logs' / 'info' / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-INFO.log"
LOGGER_ERROR_PATH = Path(
    '.'
) / 'ATRI' / 'logs' / 'error' / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-ERROR.log"
LOGGER_WARNING_PATH = Path(
    '.'
) / 'ATRI' / 'logs' / 'warning' / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-WARNING.log"

logger.add(LOGGER_INFO_PATH,
           rotation='10 MB',
           enqueue=True,
           level='INFO',
           encoding='utf-8',
           format=default_format)

logger.add(LOGGER_ERROR_PATH,
           rotation='10 MB',
           enqueue=True,
           level='ERROR',
           encoding='utf-8',
           format=default_format)

logger.add(LOGGER_WARNING_PATH,
           rotation='10 MB',
           enqueue=True,
           level='WARNING',
           encoding='utf-8',
           format=default_format)
