import random

from nonebot.plugin import on_regex, on_command
from nonebot.adapters.cqhttp.message import MessageSegment, Message
from nonebot.adapters.cqhttp import Bot
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.event import MessageEvent

from ATRI.service.plugin import Plugin
from ATRI.config import SETU_CONFIG
from ATRI.utils import compress_image
from ATRI.request import Request
from ATRI.rule import is_in_service, is_in_ban_list, is_in_dormant

from .data_source import setu_port

# ===========================[Begin Command Processing]===========================

resolution = 1


__plugin_name__ = 'setu'
__doc__ = """
涩图，开冲！
使用正则匹配
"""
Plugin.register(plugin_name=__plugin_name__, _type="func", doc=__doc__, command=SETU_CONFIG['setu']['command'])

setu = on_regex('|'.join(SETU_CONFIG['setu']['command']),
                rule=is_in_service(__plugin_name__) & is_in_ban_list()
                & is_in_dormant())

@setu.handle()
async def _(bot: Bot, event: MessageEvent) -> None:
    await bot.send(event, SETU_CONFIG['setu']['repo']['waiting'])
    rd = random.randint(1, 2)
    
    if rd == 1:
        data = await setu_port()
    else:
        data = await setu_port()

    if resolution == 1:
        img = compress_image(await Request.get_image(data['data'][0]['url']))
    else:
        img = await Request.get_image(data['data'][0]['url'])
    
    msg0 = (
        f"{data['data'][0]['title']}\n"
        f"pid: {data['data'][0]['pid']}\n"
        f"{MessageSegment.image(file=f'file:///{img}')}"
    )
    
    await setu.finish(Message(msg0))


setu_resolution = on_command(SETU_CONFIG['admin']['command'][0],
                             aliases=set(SETU_CONFIG['admin']['command']),
                             permission=SUPERUSER)

@setu_resolution.handle()
async def _(bot, event: MessageEvent, state: dict) -> None:
    msg = str(event.get_message()).strip()
    if msg:
        state['msg'] = msg

@setu_resolution.got('msg', prompt='请键入正确参数奥')
async def _(bot, event: MessageEvent, state: dict) -> None:
    global resolution
    resolution = int(state['msg'])
    
    if resolution == 1:
        await setu_resolution.finish('完成~！已启用涩图压缩')
    else:
        await setu_resolution.finish('完成~！已关闭涩图压缩')

# ===========================[End Command Processing]=============================
