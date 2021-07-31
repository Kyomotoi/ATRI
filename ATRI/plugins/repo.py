from random import choice

from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.service import Service
from ATRI.config import BotSelfConfig
from ATRI.utils.limit import FreqLimiter, DailyLimiter


_repo_flmt = FreqLimiter(20)
_repo_flmt_notice = choice(["慢...慢一..点❤", "冷静1下", "歇会歇会~~"])
_repo_dlmt = DailyLimiter(5)
_repo_dlmt_notice = "阿！不能再喝了，再喝就晕过去了！"


REPO_FORMAT = """
来自用户{user}反馈：
{msg}
"""


class Repo(Service):
    def __init__(self):
        Service.__init__(self, "反馈", "向维护者发送消息")


repo = Repo().on_command("来杯红茶", "向维护者发送消息", aliases={"反馈", "报告"})


@repo.args_parser  # type: ignore
async def _get_repo(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了", "取消"]
    if msg in quit_list:
        await repo.finish("好吧...")
    if not msg:
        await repo.reject("需要反馈的内容呢？~")
    else:
        state["repo"] = msg


@repo.handle()
async def _ready_repo(bot: Bot, event: MessageEvent, state: T_State):
    user_id = event.get_user_id()
    if not _repo_flmt.check(user_id):
        await repo.finish(_repo_flmt_notice)
    if not _repo_dlmt.check(user_id):
        await repo.finish(_repo_dlmt_notice)

    msg = str(event.message).strip()
    if msg:
        state["repo"] = msg


@repo.got("repo", "需要反馈的内容呢？~")
async def _deal_repo(bot: Bot, event: MessageEvent, state: T_State):
    msg = state["repo"]
    user_id = event.get_user_id()
    repo_0 = REPO_FORMAT.format(user=user_id, msg=msg)

    for superuser in BotSelfConfig.superusers:
        try:
            await bot.send_private_msg(user_id=superuser, message=repo_0)
        except BaseException:
            await repo.finish("发送失败了呢...")

    _repo_flmt.start_cd(user_id)
    _repo_dlmt.increase(user_id)
    await repo.finish("吾辈的心愿已由咱转告维护者！")
