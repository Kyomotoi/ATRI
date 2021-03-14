import re
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.service import Service as sv
from ATRI.rule import (
    is_block,
    is_in_dormant,
    is_in_service
)
from .data_source import roll_dice


__plugin_name__ = "roll"

roll = sv.on_command(
    name="roll一下",
    cmd="/roll",
    rule=is_block() & is_in_dormant()
    & is_in_service(__plugin_name__)
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
