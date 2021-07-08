from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.utils.apscheduler import scheduler
from .data_source import IsSurvive


ping = IsSurvive().on_command("/ping", "检测bot简单信息处理速度")


@ping.handle()
async def _ping(bot: Bot, event: MessageEvent):
    await ping.finish(IsSurvive.ping())


status = IsSurvive().on_command("/status", "查看运行资源占用")


@status.handle()
async def _status(bot: Bot, event: MessageEvent):
    msg, _ = IsSurvive.get_status()
    await status.finish(msg)


@scheduler.scheduled_job("interval", minutes=10, misfire_grace_time=15)
async def _status_checking():
    msg, stat = IsSurvive().get_status()
    if not stat:
        await status.finish(msg)
