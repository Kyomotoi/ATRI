from typing import Optional
from datetime import datetime

from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.message import run_postprocessor
from nonebot.adapters import Bot, Event

import ATRI
from ATRI.utils.apscheduler import scheduler
from .data_source import Console
from .drivers import register_route


driver = ATRI.driver()


@driver.on_bot_connect
async def _connect(bot):
    Console().store_connect_stat(True)


@driver.on_bot_disconnect
async def _disconnect(bot):
    Console().store_connect_stat(False)


msg_freq = 0
health_freq = 0
error_freq = 0


record_msg = Console().on_message(block=False)


@record_msg.handle()
async def _record_msg(bot: Bot, event: Event):
    global msg_freq
    msg_freq += 1


@run_postprocessor  # type: ignore
async def _record_is_error(
    matcher: Matcher,
    exception: Optional[Exception],
    bot: Bot,
    event: Event,
    state: T_State,
):
    global health_freq, error_freq
    if matcher.type != "message":
        if not exception:
            health_freq += 1
        else:
            error_freq += 1


@scheduler.scheduled_job("interval", minutes=1)
async def _record_data():
    global msg_freq, health_freq, error_freq
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "time": now_time,
        "freq_data": {"msg": msg_freq, "health": health_freq, "error": error_freq},
    }
    Console().record_data(data)
    msg_freq, health_freq, error_freq = 0, 0, 0


def init():
    register_route()


init()
