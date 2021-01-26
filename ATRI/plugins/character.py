from random import choice
from typing import Optional

from nonebot.plugin import on_command, on_regex
from nonebot.adapters.cqhttp import Bot, Event

from ATRI.rule import is_in_ban_list, is_in_dormant, to_bot
from ATRI.utils import count_list, del_list_aim, now_time
from ATRI.config import BOT_CONFIG, RUNTIME_CONFIG
from ATRI.service.plugin import Plugin

# ===========================[Begin Command Processing]===========================

__plugin_name__ = 'call_robot'
__doc__ = """使用正则触发"""
Plugin.register(__plugin_name__, "func", __doc__,
                        command=BOT_CONFIG['callRobot']['command'])

call_robot = on_regex('|'.join(BOT_CONFIG['callRobot']['command']),
                        rule=is_in_ban_list() & is_in_dormant(),
                        priority=4)

@call_robot.handle()
async def _(bot: Bot, event: Event) -> None:
    await bot.send(event, ATRI().call_robot(int(event.get_user_id())))


__plugin_name__ = 'call_me'
__doc__ = """正确地呼叫咱"""
Plugin.register(__plugin_name__, "func", __doc__,
                        RUNTIME_CONFIG['nickname'])

call_me = on_command(list(RUNTIME_CONFIG['nickname'])[0],
                    aliases=RUNTIME_CONFIG['nickname'],
                    rule=is_in_ban_list() & is_in_dormant())

@call_me.handle()
async def _(bot: Bot, event: Event) -> None:
    await bot.send(event, ATRI().call_me())


__plugin_name__ = 'tee_tee'
__doc__ = """一般人员不许贴！
需at"""
Plugin.register(__plugin_name__, "func", __doc__,
                        BOT_CONFIG['teetee']['command'])

teeTee = on_command(BOT_CONFIG['teetee']['command'][0],
                    aliases=set(BOT_CONFIG['teetee']['command']),
                    rule=is_in_ban_list() & is_in_dormant() & to_bot())

@teeTee.handle()
async def _(bot: Bot, event: Event) -> None:
    await bot.send(event, ATRI().tee_tee(int(event.get_user_id())))



__plugin_name__ = 'kani'
__doc__ = """カニ！カニ！！！
使用正则匹配"""
Plugin.register(__plugin_name__, "func", __doc__,
                        BOT_CONFIG['kani']['command'])

kani = on_regex('|'.join(BOT_CONFIG['kani']['command']),
                rule=is_in_ban_list() & is_in_dormant())

@kani.handle()
async def _(bot: Bot, event: Event) -> None:
    await bot.send(event, ATRI().kani())


__plugin_name__ = 'waste'
__doc__ = """不准骂咱废物
使用正则匹配，需at"""
Plugin.register(__plugin_name__, "func", __doc__,
                        BOT_CONFIG['waste']['command'])

waste = on_regex('|'.join(BOT_CONFIG['waste']['command']),
                    rule=is_in_ban_list() & is_in_dormant() & to_bot(),
                    priority=5)

@waste.handle()
async def _(bot: Bot, event: Event) -> None:
    await bot.send(event, ATRI().waste())


__plugin_name__ = 'good_morning'
__doc__ = """略带涩气的早安
需at"""
Plugin.register(__plugin_name__, "func", __doc__,
                        BOT_CONFIG['morning']['command'])

morning = on_command(BOT_CONFIG['morning']['command'][0],
                        aliases=set(BOT_CONFIG['morning']['command']),
                        rule=is_in_ban_list() & is_in_dormant() & to_bot())

@morning.handle()
async def _(bot: Bot, event: Event) -> None:
    await bot.send(event, ATRI().morning())


__plugin_name__ = 'good_noon'
__doc__ = """做白日梦
需at"""
Plugin.register(__plugin_name__, "func", __doc__,
                        BOT_CONFIG['noon']['command'])

noon = on_command(BOT_CONFIG['noon']['command'][0],
                    aliases=set(BOT_CONFIG['noon']['command']),
                    rule=is_in_ban_list() & is_in_dormant() & to_bot())

@noon.handle()
async def _(bot: Bot, event: Event) -> None:
    await bot.send(event, ATRI().noon())


__plugin_name__ = 'good_night'
__doc__ = """晚安~！
需at"""
Plugin.register(__plugin_name__, "func", __doc__,
                        BOT_CONFIG['night']['command'])

night = on_command(BOT_CONFIG['night']['command'][0],
                    aliases=set(BOT_CONFIG['night']['command']),
                    rule=is_in_ban_list() & is_in_dormant() & to_bot())

@night.handle()
async def _(bot: Bot, event: Event) -> None:
    await bot.send(event, ATRI().night())


__plugin_name__ = 'cant_do_anything'
__doc__ = """吃饭第一名！好吃就是高兴！！
使用正则匹配"""
Plugin.register(__plugin_name__, "func", __doc__,
                        BOT_CONFIG['cantdo']['command'])

cantdo = on_regex('|'.join(BOT_CONFIG['cantdo']['command']),
                    rule=is_in_ban_list() & is_in_dormant())

@cantdo.handle()
async def _(bot: Bot, event: Event) -> None:
    await bot.send(event, ATRI().cantdo())


# ===========================[End Command Processing]=============================

callrobot_list = []


class ATRI:
    def call_robot(self, user: Optional[int]) -> str:
        global callrobot_list
        result = ''
        for i in range(0, 5):
            if count_list(callrobot_list, user) == i:
                result = choice(BOT_CONFIG['callRobot']['repo'][i])
                callrobot_list.append(user)
                if count_list(callrobot_list, user) == 5:
                    callrobot_list = del_list_aim(callrobot_list, user)
                break
            else:
                continue
        return result

    def call_me(self) -> str:
        return choice(BOT_CONFIG['atri']['repo'])

    def tee_tee(self, user: Optional[int]) -> str:
        if user in RUNTIME_CONFIG['superusers']:
            return choice(BOT_CONFIG['teetee']['repo']['superusers'])
        else:
            return choice(BOT_CONFIG['teetee']['repo']['user'])

    def kani(self) -> str:
        return choice(BOT_CONFIG['kani']['repo'])

    def waste(self) -> str:
        return choice(BOT_CONFIG['waste']['repo'])

    def morning(self) -> str:
        period = BOT_CONFIG['morning']['repo']
        if period[0]['period'][0] <= now_time() < period[0]['period'][1]:
            return choice(period[0]['repo'])
        elif period[1]['period'][0] <= now_time() < period[1]['period'][1]:
            return choice(period[1]['repo'])
        elif period[2]['period'][0] <= now_time() < period[2]['period'][1]:
            return choice(period[2]['repo'])
        elif period[3]['period'][0] <= now_time() < period[3]['period'][1]:
            return choice(period[3]['repo'])
        elif period[4]['period'][0] <= now_time() < period[4]['period'][1]:
            return choice(period[4]['repo'])
        else:
            return choice(period['error'])

    def noon(self) -> str:
        if BOT_CONFIG['noon']['period'][0] <= now_time(
        ) < BOT_CONFIG['noon']['period'][1]:
            return choice(BOT_CONFIG['noon']['repo'])
        else:
            return choice(BOT_CONFIG['noon']['error'])

    def night(self) -> str:
        period = BOT_CONFIG['night']['repo']
        if period[0]['period'][0] <= now_time() < period[0]['period'][1]:
            return choice(period[0]['repo'])
        elif period[1]['period'][0] <= now_time() < period[1]['period'][1]:
            return choice(period[1]['repo'])
        elif period[2]['period'][0] <= now_time() < period[2]['period'][1]:
            return choice(period[2]['repo'])
        elif period[3]['period'][0] <= now_time() < period[3]['period'][1]:
            return choice(period[3]['repo'])
        elif period[4]['period'][0] <= now_time() < period[4]['period'][1]:
            return choice(period[4]['repo'])
        else:
            return choice(period['error'])

    def cantdo(self) -> str:
        return choice(BOT_CONFIG['cantdo']['repo'])
