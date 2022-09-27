from ATRI.database import init_database, close_database_connection
from ATRI.utils.check_update import CheckUpdate
from ATRI.log import logger as log
from ATRI.utils.apscheduler import scheduler
import ATRI

from time import sleep

driver = ATRI.driver()


@driver.on_startup
async def startup():
    await init_database()

    log.info(f"Now running: {ATRI.__version__}")

    log.info("Starting to check update...")
    commit_info = await CheckUpdate.show_latest_commit_info()
    if commit_info:
        log.info(commit_info)

    l_v, l_v_t = await CheckUpdate.show_latest_version()
    if l_v and l_v_t:
        if l_v != ATRI.__version__:
            log.warning("新版本已发布, 请更新.")
            log.warning(f"最新版本: {l_v} 更新时间: {l_v_t}")
            sleep(3)

    if not scheduler.running:
        scheduler.start()
        log.info("Scheduler Started.")

    log.info("アトリは、高性能ですから！")


@driver.on_shutdown
async def shutdown():
    await close_database_connection()

    scheduler.shutdown(False)

    log.info("Thanks for using.")
