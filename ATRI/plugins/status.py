import psutil
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.log import logger as log
from ATRI.service import Service as sv
from ATRI.rule import is_block
from ATRI.exceptions import GetStatusError
from ATRI.utils.apscheduler import scheduler
from ATRI.config import nonebot_config


ping = sv.on_command(
    name="测试机器人",
    cmd="/ping",
    rule=is_block()
)

@ping.handle()
async def _ping(bot: Bot, event: MessageEvent) -> None:
    await ping.finish("I'm fine.")


status = sv.on_command(
    name="检查机器人状态",
    cmd="/status",
    rule=is_block()
)

@status.handle()
async def _status(bot: Bot, event: MessageEvent) -> None:
    try:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        inteSENT = psutil.net_io_counters().bytes_sent / 1000000 # type: ignore
        inteRECV = psutil.net_io_counters().bytes_sent / 1000000 # type: ignore
    except GetStatusError:
        raise GetStatusError("Failed to get status.")
    
    msg = "アトリは、高性能ですから！"
    
    if cpu > 80:  # type: ignore
        msg = "咱感觉有些头晕..."
        if mem > 80:
            msg = "咱感觉有点头晕并且有点累..."
    elif mem > 80:
        msg = "咱感觉有点累..."
    elif disk > 80:
        msg = "咱感觉身体要被塞满了..."
    
    msg0 = (
        "Self status:\n"
        f"* CPU: {cpu}%\n"
        f"* MEM: {mem}%\n"
        f"* DISK: {disk}%\n"
        f"* netSENT: {inteSENT}MB\n"
        f"* netRECV: {inteRECV}MB\n"
    ) + msg
    
    await status.finish(msg0)


@scheduler.scheduled_job(
    'interval',
    minutes=5,
    misfire_grace_time=10
)
async def _():
    log.info("开始自检")
    try:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        inteSENT = psutil.net_io_counters().bytes_sent / 1000000 # type: ignore
        inteRECV = psutil.net_io_counters().bytes_sent / 1000000 # type: ignore
    except GetStatusError:
        raise GetStatusError("Failed to get status.")
    
    msg = ""
    if cpu > 80:  # type: ignore
        msg = "咱感觉有些头晕..."
        if mem > 80:
            msg = "咱感觉有点头晕并且有点累..."
    elif mem > 80:
        msg = "咱感觉有点累..."
    elif disk > 80:
        msg = "咱感觉身体要被塞满了..."
    else:
        log.info("运作正常")
        return
    
    msg0 = (
        "Self status:\n"
        f"* CPU: {cpu}%\n"
        f"* MEM: {mem}%\n"
        f"* DISK: {disk}%\n"
        f"* netSENT: {inteSENT}MB\n"
        f"* netRECV: {inteRECV}MB\n"
    ) + msg
    
    for sup in nonebot_config["superusers"]:
        await sv.NetworkPost.send_private_msg(
            user_id=sup,
            message=msg0
        )
