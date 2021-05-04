import shutil
from ATRI.log import logger as log
from ATRI.utils.apscheduler import scheduler

from .data_source import TEMP_DIR


@scheduler.scheduled_job("interval", days=7, misfire_grace_time=10)
async def clear_temp():
    log.info("正在清除涩图缓存")
    try:
        shutil.rmtree(TEMP_DIR)
        log.info("清除缓存成功！")
    except Exception:
        log.warn("清除图片缓存失败！")
