import re
from nonebot.matcher import Matcher
from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, Event

from ATRI.config import UTILS_CONFIG
from ATRI.rule import is_in_ban_list, is_in_dormant, is_in_service

from .data_source import Function

# ===========================[Begin Command Processing]===========================


__plugin_name_0__ = 'roll'
roll = on_command(UTILS_CONFIG['utils']['roll']['command'][0],
                    aliases=set(UTILS_CONFIG['utils']['roll']['command']),
                    rule=is_in_ban_list() & is_in_dormant()
                    & is_in_service(__plugin_name_0__))

__plugin_name_1__ = 'rcnb'
rcnbEncode = on_command(
                    UTILS_CONFIG['utils']['rcnb']['encode']['command'][0],
                    aliases=set(
                        UTILS_CONFIG['utils']['rcnb']['encode']['command']),
                    rule=is_in_ban_list() & is_in_dormant()
                    & is_in_service(__plugin_name_1__))

rcnbDecode = on_command(
                    UTILS_CONFIG['utils']['rcnb']['decode']['command'][0],
                    aliases=set(
                        UTILS_CONFIG['utils']['rcnb']['decode']['command']),
                    rule=is_in_ban_list() & is_in_dormant()
                    & is_in_service(__plugin_name_1__))


@roll.handle()
async def _(bot, event: Event, state: dict) -> None:
    args = str(event.get_message()).strip()
    print(args)
    if args:
        state['result'] = args

@roll.got('result', prompt='roll参数不能为空！..\ndemo: 1d10 或 2d10+3d10')
async def _(matcher: Matcher, bot: Bot, event: Event, state: dict) -> None:
    resu = state['result']
    match = re.match(r'^([\dd+\s]+?)$', resu)
    print(match)
    if not match:
        await matcher.reject('格式不-正-确！\ndemo: 1d10 或 2d10+3d10')
    await bot.send(event, Function.roll_dice(par=resu))


@rcnbEncode.handle()
async def _(bot, event: Event, state: dict) -> None:
    args = str(event.get_message()).strip()
    if args:
        state['result'] = args

@rcnbEncode.got('result', prompt='请告诉咱需要加密的字符~！')
async def _(bot: Bot, event: Event, state: dict) -> None:
    print(state['result'])
    await bot.send(event, Function.RCNB.encode(state['result']))


@rcnbDecode.handle()
async def _(bot, event: Event, state: dict) -> None:
    args = str(event.get_message()).strip()
    if args:
        state['result'] = args

@rcnbEncode.got('result', prompt='请告诉咱需要解密的字符~！')
async def _(bot: Bot, event: Event, state: dict) -> None:
    await bot.send(event, Function.RCNB.decode(state['result']))
        

# ===========================[End Command Processing]=============================
