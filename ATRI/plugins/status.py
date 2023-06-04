import os
import time
import psutil
from typing import Tuple
from datetime import datetime

from nonebot import get_bot
from nonebot.adapters.onebot.v11 import unescape

from ATRI.log import log
from ATRI.service import Service
from ATRI.message import MessageBuilder
from ATRI.exceptions import GetStatusError
from ATRI.utils import Limiter
from ATRI.utils.apscheduler import scheduler


plugin = Service("状态").document("检查 ATRI 状态")


ping = plugin.on_command("/ping", "检测 ATRI 是否存活")


@ping.handle()
async def _():
    await ping.finish("I'm fine.")


status = plugin.on_command("/status", "检查 ATRI 运行资源占用")


@status.handle()
async def _():
    msg, _ = get_status()
    print(msg)
    await status.finish(msg)


limiter = Limiter(5, 21600)


@scheduler.scheduled_job("interval", name="状态检查", minutes=30, misfire_grace_time=15)
async def _():
    log.info("检查资源消耗中...")
    msg, stat = get_status()
    if not stat:
        log.warning("资源消耗异常")

        if limiter.get_times("114514") > 5:
            return

        try:
            bot = get_bot()
        except Exception:
            bot = None
        if not limiter.check("114514"):
            msg = "状态检查提示已达限制, 将冷却 6h"

        try:
            if bot:
                await plugin.send_to_master(msg)
            limiter.increase("114514")
        except Exception:
            return
    else:
        log.info("资源消耗正常")


_STATUS_MSG = (
    MessageBuilder("[Status Overview]")
    .text("[CPU: {b_cpu}% of {p_cpu}%]")
    .text("[Memory: {b_mem} of {p_mem}%]")
    .text("[Disk usage: {p_disk}%]")
    .text("")
    .text("[Net sent: {inteSENT}MB]")
    .text("[Net recv: {inteRECV}MB]")
    .text("")
    .text("[Run Duration]")
    .text("[Bot: {bot_time}]")
    .text("[Platform: {boot_time}]")
    .text("{msg}")
    .done()
)


def get_status() -> Tuple[str, bool]:
    try:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        inte_send = psutil.net_io_counters().bytes_sent / 1000000
        inte_recv = psutil.net_io_counters().bytes_recv / 1000000

        process = psutil.Process(os.getpid())
        b_cpu = process.cpu_percent(interval=1)
        b_mem = process.memory_percent(memtype="rss")

        now = time.time()
        boot = psutil.boot_time()
        b = process.create_time()
        boot_time = str(
            datetime.utcfromtimestamp(now).replace(microsecond=0)
            - datetime.utcfromtimestamp(boot).replace(microsecond=0)
        )
        bot_time = str(
            datetime.utcfromtimestamp(now).replace(microsecond=0)
            - datetime.utcfromtimestamp(b).replace(microsecond=0)
        )
    except Exception:
        raise GetStatusError("Failed to get status.")

    msg = "アトリは、高性能ですから！"
    if cpu > 90:
        msg = "咱感觉有些头晕..."
        is_ok = False
        if mem > 90:
            msg = "咱感觉有点头晕并且有点累..."
            is_ok = False
    elif mem > 90:
        msg = "咱感觉有点累..."
        is_ok = False
    elif disk > 90:
        msg = "咱感觉身体要被塞满了..."
        is_ok = False
    else:
        is_ok = True

    msg0 = _STATUS_MSG.format(
        p_cpu=cpu,
        p_mem=mem,
        p_disk=disk,
        b_cpu=b_cpu,
        b_mem="%.1f%%" % b_mem,
        inteSENT=inte_send,
        inteRECV=inte_recv,
        bot_time=bot_time,
        boot_time=boot_time,
        msg=msg,
    )

    return unescape(msg0), is_ok
