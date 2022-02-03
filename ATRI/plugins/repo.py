from random import choice

from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message

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


reporter = Repo().on_command("来杯红茶", "向维护者发送消息", aliases={"反馈", "报告"})


@reporter.handle()
async def _ready_repo(
    matcher: Matcher, event: MessageEvent, args: Message = CommandArg()
):
    user_id = event.get_user_id()
    if not _repo_flmt.check(user_id):
        await reporter.finish(_repo_flmt_notice)
    if not _repo_dlmt.check(user_id):
        await reporter.finish(_repo_dlmt_notice)

    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("repo", args)


@reporter.got("repo", "需要反馈的内容呢？~")
async def _deal_repo(
    bot: Bot,
    event: MessageEvent,
    repo_msg: str = ArgPlainText("repo"),
):
    user_id = event.get_user_id()
    repo_0 = REPO_FORMAT.format(user=user_id, msg=repo_msg)

    for superuser in BotSelfConfig.superusers:
        try:
            await bot.send_private_msg(user_id=superuser, message=repo_0)
        except BaseException:
            await reporter.finish("发送失败了呢...")

    _repo_flmt.start_cd(user_id)
    _repo_dlmt.increase(user_id)
    await reporter.finish("吾辈的心愿已由咱转告维护者！")
