from random import choice

from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from ATRI.utils.limit import FreqLimiter
from .data_source import CodeRunner


_flmt = FreqLimiter(5)
_flmt_notice = choice(["慢...慢一..点❤", "冷静1下", "歇会歇会~~"])


code_runner = CodeRunner().on_command("/code", "在线运行一段代码，帮助：/code help")

@code_runner.handle()
async def _code_runner(bot: Bot, event: MessageEvent):
    user_id = event.get_user_id()
    if not _flmt.check(user_id):
        await code_runner.finish(_flmt_notice)
    
    msg = str(event.get_message())
    args = msg.split("\n")
    
    if not args:
        content = f"> {MessageSegment.at(user_id)}\n" + "请键入 /code help 以获取帮助~！"
    elif args[0] == "help":
        content = f"> {MessageSegment.at(user_id)}\n" + CodeRunner().help()
    elif args[0] == "list":
        content = f"> {MessageSegment.at(user_id)}\n" + CodeRunner().list_supp_lang()
    else:
        content = MessageSegment.at(user_id) + await CodeRunner().runner(msg)
    
    _flmt.start_cd(user_id)
    await code_runner.finish(Message(content))
