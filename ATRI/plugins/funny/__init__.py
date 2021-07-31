from random import choice, randint

from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from nonebot.adapters.cqhttp.message import Message

from ATRI.utils.limit import FreqLimiter, DailyLimiter
from .data_source import Funny


get_laugh = Funny().on_command("来句笑话", "隐晦的笑话...")

@get_laugh.handle()
async def _get_laugh(bot: Bot, event: MessageEvent):
    user_name = event.sender.nickname or "该裙友"
    await get_laugh.finish(await Funny().idk_laugh(user_name))


me_re_you = Funny().on_regex(r"我", "我也不懂咋解释", block=False)

@me_re_you.handle()
async def _me_re_you(bot: Bot, event: MessageEvent):
    if randint(0, 15) == 5:
        msg = str(event.get_message())
        content, is_ok = Funny().me_re_you(msg)
        if is_ok:
            await me_re_you.finish(content)


fake_msg = Funny().on_command("/fakemsg", "伪造假转发内容，格式：qq-name-content\n可构造多条，使用空格隔开，仅限群聊")

_fake_daliy_max = DailyLimiter(3)
_fake_max_notice = "不能继续下去了！明早再来"
_fake_flmt = FreqLimiter(60)
_fake_flmt_notice = choice(["慢...慢一..点❤", "冷静1下", "歇会歇会~~"])

@fake_msg.args_parser  # type: ignore
async def _perp_fake(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了"]
    if msg in quit_list:
        await fake_msg.finish("好吧...")
    if not msg:
        await fake_msg.reject("内容呢？格式：qq-name-content\n可构造多条，以上仅为一条，使用空格隔开")
    else:
        state["content"] = msg

@fake_msg.handle()
async def _ready_fake(bot: Bot, event: GroupMessageEvent, state: T_State):
    user_id = event.get_user_id()
    if not _fake_daliy_max.check(user_id):
        await fake_msg.finish(_fake_max_notice)
    if not _fake_flmt.check(user_id):
        await fake_msg.finish(_fake_flmt_notice)
    
    msg = str(event.message).strip()
    if msg:
        state["content"] = msg

@fake_msg.got("content", "内容呢？格式：qq-name-content\n可构造多条，以上仅为一条，使用空格隔开")
async def _deal_fake(bot: Bot, event: GroupMessageEvent, state: T_State):
    content = state["content"]
    group_id = event.group_id
    user_id = event.get_user_id()
    node = Funny().fake_msg(content)
    await bot.send_group_forward_msg(group_id=group_id, messages=node)
    
    _fake_flmt.start_cd(user_id)
    _fake_daliy_max.increase(user_id)


eat_what = Funny().on_regex(r"大?[今明后]天(.*?)吃[什啥]么?", "我来决定你吃什么！")

_eat_flmt = FreqLimiter(15)

@eat_what.handle()
async def _eat_what(bot: Bot, event: MessageEvent):
    user_id = event.get_user_id()
    if not _eat_flmt.check(user_id):
        return
    
    msg = str(event.get_message())
    user_name = event.sender.nickname or "裙友"
    eat = await Funny().eat_what(user_name, msg)
    _eat_flmt.start_cd(user_id)
    await eat_what.finish(Message(eat))
