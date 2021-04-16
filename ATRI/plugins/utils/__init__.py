import re
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.service import Service as sv
from ATRI.rule import is_in_service
from .data_source import roll_dice, Encrypt


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

roll = sv.on_command(
    cmd="/roll",
    docs=__doc__,
    rule=is_in_service('roll')
)

@roll.handle()
async def _roll(bot: Bot, event: MessageEvent, state: dict) -> None:
    args = str(event.message).strip()
    if args:
        state['resu'] = args

@roll.got("resu", prompt="roll 参数不能为空~！\ndemo：1d10 或 2d10+2d10")
async def _(bot: Bot, event: MessageEvent, state: dict) -> None:
    resu = state['resu']
    match = re.match(r'^([\dd+\s]+?)$', resu)
    
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

encrypt = sv.on_command(
    cmd="/enc",
    docs=__doc__,
    rule=is_in_service('enc')
)

@encrypt.handle()
async def _encrypt(bot: Bot, event: MessageEvent) -> None:
    msg = str(event.message).split(' ')
    _type = msg[0]
    s = msg[1]
    e = Encrypt()
    
    if _type == "e":
        await encrypt.finish(e.encode(s))
    elif _type == "d":
        await encrypt.finish(e.decode(s))
    else:
        await encrypt.finish('请检查输入~！')
