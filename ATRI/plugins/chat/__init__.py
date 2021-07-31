from random import choice

from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.utils import CoolqCodeChecker
from ATRI.utils.limit import FreqLimiter
from ATRI.utils.apscheduler import scheduler
from .data_source import Chat


_chat_flmt = FreqLimiter(3)
_chat_flmt_notice = choice(["慢...慢一..点❤", "冷静1下", "歇会歇会~~", "我开始为你以后的伴侣担心了..."])


chat = Chat().on_message("闲聊（文爱")

@chat.handle()
async def _chat(bot: Bot, event: MessageEvent):
    print(1)
    user_id = event.get_user_id()
    if not _chat_flmt.check(user_id):
        await chat.finish(_chat_flmt_notice)
    
    msg = str(event.message)
    repo = await Chat().deal(msg, user_id)
    _chat_flmt.start_cd(user_id)
    await chat.finish(repo)

my_name_is = Chat().on_command("叫我", "更改闲聊（划掉 文爱）时的称呼", aliases={"我是"}, priority=1)

@my_name_is.args_parser  # type: ignore
async def _get_name(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了", "取消"]
    if msg in quit_list:
        await my_name_is.finish("好吧...")
    if not msg:
        await my_name_is.reject("欧尼酱想让咱如何称呼呢！0w0")
    else:
        state["name"] = msg

@my_name_is.handle()
async def _name(bot: Bot, event: MessageEvent, state: T_State):
    user_id = event.get_user_id()
    if not _chat_flmt.check(user_id):
        await my_name_is.finish(_chat_flmt_notice)
    
    msg = str(event.message).strip()
    if msg:
        state["name"] = msg

@my_name_is.got("name", "欧尼酱想让咱如何称呼呢！0w0")
async def _deal_name(bot: Bot, event: MessageEvent, state: T_State):
    user_id = event.get_user_id()
    new_name = state["name"]
    repo = choice([
        f"好~w 那咱以后就称呼你为{new_name}！",
        f"噢噢噢！原来你叫{new_name}阿~",
        f"好欸！{new_name}ちゃん~~~",
        "很不错的称呼呢w"
    ])
    Chat().name_is(user_id, new_name)
    _chat_flmt.start_cd(user_id)
    await my_name_is.finish(repo)


say = Chat().on_command("说", "别人让我说啥就说啥（", priority=1)

@say.args_parser  # type: ignore
async def _get_say(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了"]
    if msg in quit_list:
        await say.finish("好吧...")
    if not msg:
        await say.reject("阿！要咱说啥呢...")
    else:
        state["say"] = msg

@say.handle()
async def _ready_say(bot: Bot, event: MessageEvent, state: T_State):
    user_id = event.get_user_id()
    if not _chat_flmt.check(user_id):
        await say.finish(_chat_flmt_notice)
    
    msg = str(event.message)
    if msg:
        state["say"] = msg

@say.got("say")
async def _deal_say(bot: Bot, event: MessageEvent, state: T_State):
    msg = state["say"]
    check = CoolqCodeChecker(msg).check
    if not check:
        repo = choice([
            "不要...",
            "这个咱不想复读！",
            "不可以",
            "不好！"
        ])
        await say.finish(repo)
    
    user_id = event.get_user_id()
    _chat_flmt.start_cd(user_id)
    await say.finish(msg)


@scheduler.scheduled_job("interval", hours=3, misfire_grace_time=60)
async def _check_kimo():
    try:
        await Chat().update_data()
    except BaseException:
        pass
