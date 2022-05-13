from typing import Optional

from nonebot.message import run_postprocessor

from ATRI.utils.apscheduler import scheduler
from .models import MessageDealerInfo


recv_msg = int()
deal_msg = int()
failed_deal_msg = int()

total_r_m = int()
total_d_m = int()
total_f_m = int()


@run_postprocessor
async def _(exception: Optional[Exception]):
    global recv_msg, deal_msg, failed_deal_msg, total_r_m, total_d_m, total_f_m

    if exception:
        failed_deal_msg += 1
        total_f_m += 1
    else:
        deal_msg += 1
        total_d_m += 1

    recv_msg += 1
    total_r_m += 1


def get_message_deal_info() -> dict:
    return MessageDealerInfo(
        recv_msg=str(recv_msg),
        deal_msg=str(deal_msg),
        failed_deal_msg=str(failed_deal_msg),
        total_r_m=str(total_r_m),
        total_d_m=str(total_d_m),
        total_f_m=str(total_f_m),
    ).dict()


@scheduler.scheduled_job("interval", name="信息数据重置", seconds=15, misfire_grace_time=1)  # type: ignore
async def _():
    global recv_msg, deal_msg, failed_deal_msg
    recv_msg = int()
    deal_msg = int()
    failed_deal_msg = int()
