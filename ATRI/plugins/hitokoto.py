import json
from pathlib import Path
from random import choice, randint

from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, Event

from ATRI.exceptions import InvalidLoad
from ATRI.rule import is_in_ban_list, is_in_dormant, is_in_service, to_bot
from ATRI.utils import del_list_aim, count_list
from ATRI.request import Request
from ATRI.config import HITOKOTO_CONFIG
from ATRI.service.plugin import Plugin

# ===========================[Begin Command Processing]===========================


__plugin_name__ = 'hitokoto'
__doc__ = """一言"""
Plugin.register(__plugin_name__, "func", __doc__,
         HITOKOTO_CONFIG['hitokoto']['command'])

hitokoto = on_command(HITOKOTO_CONFIG['hitokoto']['command'][0],
                        aliases=set(HITOKOTO_CONFIG['hitokoto']['command']),
                        rule=is_in_ban_list() & is_in_dormant()
                        & is_in_service(__plugin_name__)
                        & to_bot())

@hitokoto.handle()
async def _(bot: Bot, event: Event) -> None:
    await bot.send(event, await Function().hitokoto(str(event.get_user_id())))


# ===========================[End Command Processing]=============================

hitokoto_list = []
local_path = Path('.') / 'ATRI' / 'data' / 'database' / 'hitokoto'

class Function:
    async def hitokoto(self, user: str):
        def local() -> str:
            rd = choice(HITOKOTO_CONFIG['hitokoto']['local']['file'])
            path = local_path / f"{rd}"
            data = {}
            try:
                data = json.loads(path.read_bytes())
            except InvalidLoad:
                raise InvalidLoad('Failed to read file!')
            return data[randint(1, len(data)) - 1]['hitokoto']
        
        async def link() -> str:
            url = HITOKOTO_CONFIG['hitokoto']['link']['url']
            return str(
                await Request.get_text(
                    url=url
                )
            )
        
        global hitokoto_list

        if count_list(hitokoto_list, user) == 3:
            hitokoto_list.append(user)
            return choice(HITOKOTO_CONFIG['hitokoto']['times'][3]['repo'])
        elif count_list(hitokoto_list, user) == 6:
            hitokoto_list = del_list_aim(hitokoto_list, user)
            return choice(HITOKOTO_CONFIG['hitokoto']['times'][6]['repo'])
        else:
            hitokoto_list.append(user)
            if HITOKOTO_CONFIG['hitokoto']['link']['use']:
                rd = randint(1,2)
                if rd == 1:
                    return await link()
                else:
                    return local()
            else:
                return local()
