import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from nonebot.log import LoguruHandler


scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")


aps_logger = logging.getLogger("apscheduler")
aps_logger.setLevel(logging.DEBUG)
aps_logger.handlers.clear()
aps_logger.addHandler(LoguruHandler())
