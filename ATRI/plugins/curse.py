from random import choice
from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot

from ATRI.request import Request
from ATRI.utils import count_list, del_list_aim
from ATRI.config import CURSE_CONFIG
from ATRI.exceptions import InvalidRequest
from ATRI.service.plugin import Plugin
from ATRI.rule import is_in_ban_list, is_in_service, is_in_dormant, to_bot



# ===========================[Begin Command Processing]===========================


__plugin_name__ = 'curse'
__doc__ = """口臭一下"""
Plugin.register(__plugin_name__, "func", __doc__,
                        CURSE_CONFIG['curse']['command'])

curse = on_command(CURSE_CONFIG['curse']['command'][0],
                    aliases=set(CURSE_CONFIG['curse']['command']),
                    rule=is_in_ban_list() & is_in_dormant()
                    & is_in_service(__plugin_name__)
                    & to_bot())

@curse.handle()
async def _(bot: Bot, event) -> None:
    await bot.send(
        event, await Function().curse(str(event.get_user_id())))


# ===========================[End Command Processing]=============================

curse_list = []


class Function:
    async def curse(self, user: str):
        global curse_list
        
        if count_list(curse_list, user) == 3:
            curse_list.append(user)
            return choice(CURSE_CONFIG['curse']['times'][3]['repo'])
        elif count_list(curse_list, user) == 6:
            curse_list = del_list_aim(curse_list, user)
            return choice(CURSE_CONFIG['curse']['times'][6]['repo'])
        else:
            try:
                curse_list.append(user)
                return str(await Request.get_text(
                    url=CURSE_CONFIG['curse']['url']))
            except InvalidRequest:
                raise InvalidRequest('请求失败')
