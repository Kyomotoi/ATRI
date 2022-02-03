from random import choice

from nonebot.matcher import Matcher
from nonebot.params import ArgPlainText, CommandArg
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message

from ATRI.utils.limit import FreqLimiter
from ATRI.utils.apscheduler import scheduler
from .data_source import Chat

_chat_flmt = FreqLimiter(3)
_chat_flmt_notice = choice(["慢...慢一..点❤", "冷静1下", "歇会歇会~~", "我开始为你以后的伴侣担心了..."])


chat = Chat().on_message("文爱", "闲聊（文爱")


@chat.handle()
async def _chat(bot: Bot, event: MessageEvent):
    user_id = event.get_user_id()
    if not _chat_flmt.check(user_id):
        await chat.finish(_chat_flmt_notice)

    msg = str(event.message)
    repo = await Chat().deal(msg, user_id)
    _chat_flmt.start_cd(user_id)
    try:
        await chat.finish(repo)
    except Exception:
        return


my_name_is = Chat().on_command("叫我", "更改闲聊（文爱）时的称呼", aliases={"我是"}, priority=1)


@my_name_is.handle()
async def _name(matcher: Matcher, event: MessageEvent, args: Message = CommandArg()):
    user_id = event.get_user_id()
    if not _chat_flmt.check(user_id):
        await my_name_is.finish(_chat_flmt_notice)

    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("name", args)


@my_name_is.got("name", "欧尼酱想让咱如何称呼呢！0w0")
async def _deal_name(event: MessageEvent, new_name: str = ArgPlainText("name")):
    user_id = event.get_user_id()
    repo = choice(
        [
            f"好~w 那咱以后就称呼你为{new_name}！",
            f"噢噢噢！原来你叫{new_name}阿~",
            f"好欸！{new_name}ちゃん~~~",
            "很不错的称呼呢w",
        ]
    )
    Chat().name_is(user_id, new_name)
    _chat_flmt.start_cd(user_id)
    await my_name_is.finish(repo)


say = Chat().on_command("说", "别人让我说啥就说啥（", priority=1)


@say.handle()
async def _ready_say(
    matcher: Matcher, event: MessageEvent, args: Message = CommandArg()
):
    user_id = event.get_user_id()
    if not _chat_flmt.check(user_id):
        await say.finish(_chat_flmt_notice)

    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("say", args)


@say.got("say", "想要咱复读啥呢...")
async def _deal_say(event: MessageEvent, msg: str = ArgPlainText("say")):
    user_id = event.get_user_id()
    _chat_flmt.start_cd(user_id)
    await say.finish(msg)


@scheduler.scheduled_job("interval", name="闲聊词库检查更新", hours=3, misfire_grace_time=60)
async def _check_kimo():
    try:
        await Chat().update_data()
    except BaseException:
        pass
