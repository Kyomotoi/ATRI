import ATRI
from ATRI.log import log
from ATRI.utils.apscheduler import scheduler
from ATRI.utils.check_update import CheckUpdate
from ATRI.database import init_database, close_database_connection

from time import sleep

from ATRI.patch import *

driver = ATRI.driver()


@driver.on_startup
async def startup():
    await init_database()

    log.info(f"当前版本: {ATRI.__version__}")

    log.info("开始检查更新...")
    commit_info = await CheckUpdate.show_latest_commit_info()
    if commit_info:
        log.info(commit_info)

    l_v, l_v_t = await CheckUpdate.show_latest_version()
    if l_v and l_v_t:
        if l_v != ATRI.__version__:
            log.warning("新版本已发布, 请更新")
            log.warning(f"最新版本: {l_v} 更新时间: {l_v_t}")
            sleep(3)

    if not scheduler.running:
        scheduler.start()
        log.info("定时任务已启用")

    log.info("アトリは、高性能ですから！")


@driver.on_shutdown
async def shutdown():
    await close_database_connection()

    scheduler.shutdown(False)

    log.info("感谢使用")
