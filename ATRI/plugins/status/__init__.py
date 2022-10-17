from nonebot import get_bot

from ATRI import conf
from ATRI.log import log
from ATRI.service import Service
from ATRI.utils.apscheduler import scheduler

from .data_source import Status


stat = Service("状态").document("检查自身状态")


ping = stat.on_command("/ping", "检测bot简单信息处理速度")


@ping.handle()
async def _():
    await ping.finish(Status.ping())


status = stat.on_command("/status", "查看运行资源占用")


@status.handle()
async def _():
    msg, _ = Status.get_status()
    await status.finish(msg)


info_msg = "アトリは高性能ですから！"


@scheduler.scheduled_job("interval", name="状态检查", minutes=10, misfire_grace_time=15)  # type: ignore
async def _():
    log.info("开始检查资源消耗...")
    msg, stat = Status.get_status()
    if not stat:
        log.warning(msg)

        bot = get_bot()
        for super in conf.BotConfig.superusers:
            await bot.send_private_msg(user_id=super, message=msg)

    log.info("资源消耗正常")
