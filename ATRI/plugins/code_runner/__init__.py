from random import choice

from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import MessageEvent, Message, MessageSegment, unescape
from nonebot.adapters.onebot.v11.helpers import Cooldown

from ATRI.service import Service

from .data_source import CodeRunner


plugin = Service("在线跑代码").document("在线运行代码").main_cmd("/code")

_flmt_notice = choice(["慢...慢一..点❤", "冷静1下", "歇会歇会~~"])


code_runner = plugin.on_command("/code", "在线运行一段代码，获取帮助：/code.help")


@code_runner.handle([Cooldown(5, prompt=_flmt_notice)])
async def _code_runner(matcher: Matcher, args: Message = CommandArg()):
    msg = args.extract_plain_text()

    if msg:
        matcher.set_arg("opt", args)
    else:
        content = "请键入 /code.help 以获取帮助~！"
        await code_runner.finish(Message(content))


@code_runner.got("opt", prompt="需要运行的语言及代码？\n获取帮助：/code.help")
async def _(event: MessageEvent, opt: str = ArgPlainText("opt")):
    user_id = event.get_user_id()

    # 拯救傻瓜用户
    if opt == "/code.help":
        await code_runner.finish(CodeRunner().help())

    content = MessageSegment.at(user_id) + str(await CodeRunner().runner(unescape(opt)))
    await code_runner.finish(Message(content))


code_runner_helper = plugin.cmd_as_group("help", "使用说明")


@code_runner_helper.handle()
async def _():
    await code_runner_helper.finish(CodeRunner().help())


code_supp_list = plugin.cmd_as_group("list", "查看支持的语言")


@code_supp_list.handle()
async def _():
    await code_supp_list.finish(CodeRunner().list_supp_lang())
