import re
from random import random

from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.service import Service as sv
from ATRI.rule import is_in_service
from .data_source import roll_dice, Encrypt, Yinglish


__doc__ = """
roll一下
权限组：所有人
用法：
  /roll (int)d(int)+...
补充：
  int: 阿拉伯数字
示例：
  /roll 1d10+10d9+4d5+2d3
"""

roll = sv.on_command(cmd="/roll", docs=__doc__, rule=is_in_service("roll"))


@roll.args_parser  # type: ignore
async def _load_roll(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了", "取消"]
    if msg in quit_list:
        await roll.finish("好吧...")
    if not msg:
        await roll.reject("点呢？（1d10+...）")
    else:
        state["resu"] = msg


@roll.handle()
async def _roll(bot: Bot, event: MessageEvent, state: T_State) -> None:
    args = str(event.message).strip()
    if args:
        state["resu"] = args


@roll.got("resu", prompt="roll 参数不能为空~！\ndemo：1d10 或 2d10+2d10")
async def _deal_roll(bot: Bot, event: MessageEvent, state: T_State) -> None:
    resu = state["resu"]
    match = re.match(r"^([\dd+\s]+?)$", resu)

    if not match:
        await roll.finish("请输入正确的参数！！\ndemo：1d10 或 2d10+2d10")

    await roll.finish(roll_dice(resu))


__doc__ = """
加密传输（bushi
权限组：所有人
用法：
  /enc e,d msg
补充：
  e,d：对应 编码/解码
  msg: 目标内容
示例：
  /enc e アトリは高性能ですから！
"""

encrypt = sv.on_command(cmd="/enc", docs=__doc__, rule=is_in_service("enc"))


@encrypt.handle()
async def _encrypt(bot: Bot, event: MessageEvent) -> None:
    msg = str(event.message).split(" ")
    _type = msg[0]
    s = msg[1]
    e = Encrypt()

    if _type == "e":
        await encrypt.finish(e.encode(s))
    elif _type == "d":
        await encrypt.finish(e.decode(s))
    else:
        await encrypt.finish("请检查输入~！")


__doc__ = """
涩批一下！
权限组：所有人
用法：
  涩批一下 (msg)
"""

sepi = sv.on_command(cmd="涩批一下", docs=__doc__, rule=is_in_service("涩批一下"))


@sepi.handle()
async def _load_sepi(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了", "取消"]
    if msg in quit_list:
        await sepi.finish("好吧...")
    if not msg:
        await sepi.reject("话呢？")
    else:
        state["sepi_msg"] = msg


@sepi.handle()
async def _sepi(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["sepi_msg"] = msg


@sepi.got("sepi_msg", prompt="话呢？")
async def _deal_sepi(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = state["sepi_msg"]
    if len(msg) < 4:
        await sepi.finish("这么短？涩不起来！")
    await sepi.finish(Yinglish.deal(msg, random()))
