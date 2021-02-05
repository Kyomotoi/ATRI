# Fork from: https://github.com/nonebot/plugin-apscheduler

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from nonebot import get_driver, export
from nonebot.log import logger, LoguruHandler


apscheduler_autostart: bool = True
apscheduler_config: dict = {"apscheduler.timezone": "Asia/Shanghai"}


driver = get_driver()
scheduler = AsyncIOScheduler()
export().scheduler = scheduler


async def _start_scheduler():
    if not scheduler.running:
        scheduler.configure(apscheduler_config)
        scheduler.start()
        logger.info("Scheduler Started.")


if apscheduler_autostart:
    driver.on_startup(_start_scheduler)

aps_logger = logging.getLogger("apscheduler")
aps_logger.setLevel(logging.DEBUG)
aps_logger.handlers.clear()
aps_logger.addHandler(LoguruHandler())

from apscheduler.triggers.date import DateTrigger
