import psutil

from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.rule import is_in_banlist
from ATRI.exceptions import GetStatusError


ping = on_command("/ping", rule=is_in_banlist())

@ping.handle()
async def _ping(bot: Bot, event: MessageEvent) -> None:
    await ping.finish("I'm fine.")


status = on_command("/status", rule=is_in_banlist())

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
