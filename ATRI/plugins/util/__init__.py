import re
from random import choice, random

from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.utils.limit import FreqLimiter
from .data_source import Encrypt, Utils, Yinglish


roll = Utils().on_command("/roll", "骰子~用法：1d10 或 2d10+2d10+more")


@roll.args_parser  # type: ignore
async def _get_roll(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了"]
    if msg in quit_list:
        await roll.finish("好吧...")
    if not msg:
        await roll.reject("参数呢？！格式：1d10 或 2d10+2d10+more")
    else:
        state["roll"] = msg


@roll.handle()
async def _ready_roll(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["roll"] = msg


@roll.got("roll", "参数呢？！格式：1d10 或 2d10+2d10+more")
async def _deal_roll(bot: Bot, event: MessageEvent, state: T_State):
    text = state["roll"]
    match = re.match(r"^([\dd+\s]+?)$", text)

    if not match:
        await roll.finish("阿——！参数不对！格式：1d10 或 2d10+2d10+more")

    msg = Utils().roll_dice(text)
    await roll.finish(msg)


encrypt_en = Utils().on_command("加密", "我们之前的秘密❤")


@encrypt_en.args_parser  # type: ignore
async def _get_encr_en_text(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了"]
    if msg in quit_list:
        await roll.finish("好吧...")
    if not msg:
        await roll.reject("内容呢？！")
    else:
        state["encr_en_text"] = msg


@encrypt_en.handle()
async def _ready_en(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["encr_en_text"] = msg


@encrypt_en.got("encr_en_text", "内容呢？！")
async def _deal_en(bot: Bot, event: MessageEvent, state: T_State):
    text = state["encr_en_text"]
    is_ok = len(text)
    if is_ok < 10:
        await encrypt_en.reject("太短不加密！")
    en = Encrypt()
    result = en.encode(text)
    await encrypt_en.finish(result)


encrypt_de = Utils().on_command("解密", "解开我们的秘密❤")


@encrypt_de.args_parser  # type: ignore
async def _get_encr_de_text(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了"]
    if msg in quit_list:
        await encrypt_de.finish("好吧...")
    if not msg:
        await encrypt_de.reject("内容呢？！")
    else:
        state["encr_de_text"] = msg


@encrypt_de.handle()
async def _ready_de(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["encr_de_text"] = msg


@encrypt_de.got("encr_de_text", "内容呢？！")
async def _deal_de(bot: Bot, event: MessageEvent, state: T_State):
    text = state["encr_de_text"]
    en = Encrypt()
    result = en.decode(text)
    await encrypt_de.finish(result)


sepi = Utils().on_command("涩批一下", "将正常的句子涩一涩~")

_sepi_flmt = FreqLimiter(3)
_sepi_flmt_notice = ["涩批爬", "✌🥵✌"]


@sepi.args_parser  # type: ignore
async def _get_sepi(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了", "取消"]
    if msg in quit_list:
        await sepi.finish("好吧...")
    if not msg:
        await sepi.reject("内容呢？！")
    else:
        state["sepi_text"] = msg


@sepi.handle()
async def _ready_sepi(bot: Bot, event: MessageEvent, state: T_State):
    user_id = event.get_user_id()
    if not _sepi_flmt.check(user_id):
        await sepi.finish(choice(_sepi_flmt_notice))

    msg = str(event.message).strip()
    if msg:
        state["sepi_text"] = msg


@sepi.got("sepi_text", "内容呢？！")
async def _deal_sepi(bot: Bot, event: MessageEvent, state: T_State):
    user_id = event.get_user_id()
    msg = state["sepi_text"]
    if len(msg) < 4:
        await sepi.finish("这么短？涩不起来！")

    result = Yinglish.deal(msg, random())
    _sepi_flmt.start_cd(user_id)
    await sepi.finish(result)
