from random import choice

from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import MessageEvent, Message, MessageSegment, unescape

from ATRI.utils.limit import FreqLimiter
from .data_source import CodeRunner


_flmt = FreqLimiter(5)
_flmt_notice = choice(["慢...慢一..点❤", "冷静1下", "歇会歇会~~"])


code_runner = CodeRunner().on_command("/code", "在线运行一段代码，帮助：/code help")


@code_runner.handle()
async def _code_runner(matcher: Matcher, event: MessageEvent, args: Message = CommandArg()):
    user_id = event.get_user_id()
    if not _flmt.check(user_id):
        await code_runner.finish(_flmt_notice)
    
    msg = args.extract_plain_text()
    print(msg, args, type(msg), type(args))
    if msg:
        matcher.set_arg("opt", args)
    else:
        content = f"> {MessageSegment.at(user_id)}\n" + "请键入 /code help 以获取帮助~！"
        await code_runner.finish(Message(content))


@code_runner.got("opt")
async def _(event: MessageEvent, opt: str = ArgPlainText("opt")):
    user_id = event.get_user_id()
    msg = opt.split("\n")

    
    if msg[0] == "help":
        content = f"> {MessageSegment.at(user_id)}\n" + "请键入 /code help 以获取帮助~！"
    elif msg[0] == "list":
        content = f"> {MessageSegment.at(user_id)}\n" + CodeRunner().list_supp_lang()
    else:
        content = MessageSegment.at(user_id) + await CodeRunner().runner(unescape(opt))

    _flmt.start_cd(user_id)
    await code_runner.finish(Message(content))
