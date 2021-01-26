from nonebot.plugin import on_regex
from nonebot.adapters.cqhttp import Bot
from nonebot.adapters.cqhttp.event import MessageEvent

from ATRI.service.plugin import Plugin
from ATRI.config import SETU_CONFIG
from ATRI.rule import is_in_service, is_in_ban_list, is_in_dormant

# ===========================[Begin Command Processing]===========================


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
    
    

# ===========================[End Command Processing]=============================