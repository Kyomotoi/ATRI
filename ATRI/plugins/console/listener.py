from typing import Optional
from pydantic import BaseModel

from nonebot.message import run_postprocessor

from ATRI.utils.apscheduler import scheduler


interval_deal_message = int()
interval_recv_message = int()
interval_failed_message = int()

total_deal_message = int()
total_recv_message = int()
total_failed_message = int()


@run_postprocessor
async def _(exception: Optional[Exception]):
    global interval_deal_message, interval_recv_message, interval_failed_message
    global total_deal_message, total_recv_message, total_failed_message

    if exception:
        interval_failed_message += 1
        total_failed_message += 1
    else:
        interval_deal_message += 1
        total_deal_message += 1

    interval_recv_message += 1
    total_recv_message += 1


@scheduler.scheduled_job("interval", name="消息统计数据重置", seconds=15, misfire_grace_time=30)
async def _():
    global interval_deal_message, interval_recv_message, interval_failed_message

    interval_deal_message = 0
    interval_recv_message = 0
    interval_failed_message = 0


class MessageInfo(BaseModel):
    interval_deal: int
    interval_recv: int
    interval_failed: int

    total_deal: int
    total_recv: int
    total_failed: int


def get_message_info() -> MessageInfo:
    return MessageInfo(
        interval_deal=interval_deal_message,
        interval_recv=interval_recv_message,
        interval_failed=interval_failed_message,
        total_deal=total_deal_message,
        total_recv=total_deal_message,
        total_failed=total_failed_message,
    )
