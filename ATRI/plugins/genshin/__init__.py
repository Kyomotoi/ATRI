import re
from nonebot.plugin import on_command
from nonebot.typing import Bot, Event

from ATRI.config import GENSHIN_CONFIG
from ATRI.exceptions import InvalidRequestError
from ATRI.rule import isInBanList, isInDormant, isInService

from .data_source import Genshin

__plugin_name__ = 'genshin'

genshin = on_command(GENSHIN_CONFIG['genshin']['command'][0],
                     aliases=set(GENSHIN_CONFIG['genshin']['command']),
                     rule=isInBanList() & isInDormant()
                     & isInService(__plugin_name__))


@genshin.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    args = str(event.message)
    
    if args:
        state['args'] = args

@genshin.got('args', prompt='请告诉咱id以及是官服还是b服嗷~w\n用空格隔开！！')
async def _(bot: Bot, event: Event, state: dict) -> None:
    args = state['args'].split(' ')
    uid_info = ''
    server_id = ''
    
    if len(args[0]) != 9:
        await genshin.finish('抱歉暂时只支持国服呢...')
    else:
        pass
    
    if re.findall('[Bb官]服', args[1]):
        if re.findall('[Bb]服', args[1]):
            server_id = 'cn_qd01'
        else:
            server_id = 'cn_gf01'
        
        await bot.send(event, '别急，在找！')
        try:
            uid_info = Genshin().jsonAnalysis(Genshin().getInfo(server_id=server_id, uid=args[0]))
        except InvalidRequestError:
            await genshin.finish('找不到呢...咱搜索区域或许出错了...')
        
        msg0 = (f'{args[0]} Genshin INFO:\n'
                f'{uid_info}')
        await genshin.finish(msg0)
    else:
        await genshin.finish('抱歉暂时只支持官服和b服...呐.')
