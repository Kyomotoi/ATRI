from random import choice

from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from nonebot.adapters.onebot.v11.helpers import Cooldown

from ATRI import conf
from ATRI.service import Service
from ATRI.message import MessageBuilder


_repo_flmt_notice = choice(["慢...慢一..点❤", "冷静1下", "歇会歇会~~"])


_REPO_FORMAT = (
    MessageBuilder("来自用户{user}反馈:")
    .text("{msg}")
    .text("- 如有类似 CQ 一类关键词出现")
    .text("- 无需担心, 关注其它内容即可")
    .done()
)
_REPO_FORMAT = MessageBuilder("来自用户{user}反馈:").text("{msg}").done()


repo = Service("反馈").document("向维护者发送消息")


reporter = repo.on_command("来杯红茶", "向维护者发送消息", aliases={"反馈", "报告"})


@reporter.handle([Cooldown(120, prompt=_repo_flmt_notice)])
async def _ready_repo(matcher: Matcher, args: Message = CommandArg()):
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
    repo_0 = _REPO_FORMAT.format(user=user_id, msg=repo_msg)

    for superuser in conf.BotConfig.superusers:
        try:
            await bot.send_private_msg(user_id=superuser, message=repo_0)
        except Exception:
            await reporter.finish("发送失败了呢...")

    await reporter.finish("吾辈的心愿已由咱转告维护者！")
