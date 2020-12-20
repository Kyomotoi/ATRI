from random import choice
from typing import Optional

from nonebot.typing import Bot, Event
from nonebot.plugin import on_command, on_regex

from ATRI.rule import isInBanList, isInDormant, toBot
from ATRI.utils import countList, delListAim, nowTime
from ATRI.config import BOT_CONFIG, NONEBOT_CONFIG

# ===========================[Begin Command Processing]===========================


class Action:
    callRobot = on_regex('|'.join(BOT_CONFIG['callRobot']['command']),
                         rule=isInBanList() & isInDormant(),
                         priority=4)

    callMe = on_command(list(NONEBOT_CONFIG['nickname'])[0],
                        aliases=NONEBOT_CONFIG['nickname'],
                        rule=isInBanList() & isInDormant())

    teeTee = on_command(BOT_CONFIG['teetee']['command'][0],
                        aliases=set(BOT_CONFIG['teetee']['command']),
                        rule=isInBanList() & isInDormant() & toBot())

    kani = on_regex('|'.join(BOT_CONFIG['kani']['command']),
                    rule=isInBanList() & isInDormant())

    waste = on_regex('|'.join(BOT_CONFIG['waste']['command']),
                     rule=isInBanList() & isInDormant() & toBot(),
                     priority=5)

    morning = on_command(BOT_CONFIG['morning']['command'][0],
                         aliases=set(BOT_CONFIG['morning']['command']),
                         rule=isInBanList() & isInDormant() & toBot())

    noon = on_command(BOT_CONFIG['noon']['command'][0],
                      aliases=set(BOT_CONFIG['noon']['command']),
                      rule=isInBanList() & isInDormant() & toBot())

    night = on_command(BOT_CONFIG['night']['command'][0],
                       aliases=set(BOT_CONFIG['night']['command']),
                       rule=isInBanList() & isInDormant() & toBot())

    cantdo = on_regex('|'.join(BOT_CONFIG['cantdo']['command']),
                      rule=isInBanList() & isInDormant())

    @callRobot.handle()
    async def _(bot: Bot, event: Event, state: dict) -> None:
        await bot.send(event, ATRI()._callRobot(event.user_id))

    @callMe.handle()
    async def _(bot: Bot, event: Event, state: dict) -> None:
        await bot.send(event, ATRI()._callMe())

    @teeTee.handle()
    async def _(bot: Bot, event: Event, state: dict) -> None:
        await bot.send(event, ATRI()._teeTee(event.user_id))

    @kani.handle()
    async def _(bot: Bot, event: Event, state: dict) -> None:
        await bot.send(event, ATRI()._kani())

    @waste.handle()
    async def _(bot: Bot, event: Event, state: dict) -> None:
        await bot.send(event, ATRI()._waste())

    @morning.handle()
    async def _(bot: Bot, event: Event, state: dict) -> None:
        await bot.send(event, ATRI()._morning())

    @noon.handle()
    async def _(bot: Bot, event: Event, state: dict) -> None:
        await bot.send(event, ATRI()._noon())

    @night.handle()
    async def _(bot: Bot, event: Event, state: dict) -> None:
        await bot.send(event, ATRI()._night())
    
    @cantdo.handle()
    async def _(bot: Bot, event: Event, state: dict) -> None:
        await bot.send(event, ATRI()._cantdo())


# ===========================[End Command Processing]===========================

callrobot_list = []


class ATRI():
    def _callRobot(self, user: Optional[int]) -> str:
        global callrobot_list
        result = ''
        for i in range(0, 5):
            if countList(callrobot_list, user) == i:
                result = choice(BOT_CONFIG['callRobot']['repo'][i])
                callrobot_list.append(user)
                if countList(callrobot_list, user) == 5:
                    callrobot_list = delListAim(callrobot_list, user)
                break
            else:
                continue
        return result

    def _callMe(self) -> str:
        return choice(BOT_CONFIG['atri']['repo'])

    def _teeTee(self, user: Optional[int]) -> str:
        if user in NONEBOT_CONFIG['superusers']:
            return choice(BOT_CONFIG['teetee']['repo']['superusers'])
        else:
            return choice(BOT_CONFIG['teetee']['repo']['user'])

    def _kani(self) -> str:
        return choice(BOT_CONFIG['kani']['repo'])

    def _waste(self) -> str:
        return choice(BOT_CONFIG['waste']['repo'])

    def _morning(self) -> str:
        period = BOT_CONFIG['morning']['repo']
        if period[0]['period'][0] <= nowTime() < period[0]['period'][1]:
            return choice(period[0]['repo'])
        elif period[1]['period'][0] <= nowTime() < period[1]['period'][1]:
            return choice(period[1]['repo'])
        elif period[2]['period'][0] <= nowTime() < period[2]['period'][1]:
            return choice(period[2]['repo'])
        elif period[3]['period'][0] <= nowTime() < period[3]['period'][1]:
            return choice(period[3]['repo'])
        elif period[4]['period'][0] <= nowTime() < period[4]['period'][1]:
            return choice(period[4]['repo'])
        else:
            return choice(period['error'])

    def _noon(self) -> str:
        if BOT_CONFIG['noon']['period'][0] <= nowTime(
        ) < BOT_CONFIG['noon']['period'][1]:
            return choice(BOT_CONFIG['noon']['repo'])
        else:
            return choice(BOT_CONFIG['noon']['error'])

    def _night(self) -> str:
        period = BOT_CONFIG['night']['repo']
        if period[0]['period'][0] <= nowTime() < period[0]['period'][1]:
            return choice(period[0]['repo'])
        elif period[1]['period'][0] <= nowTime() < period[1]['period'][1]:
            return choice(period[1]['repo'])
        elif period[2]['period'][0] <= nowTime() < period[2]['period'][1]:
            return choice(period[2]['repo'])
        elif period[3]['period'][0] <= nowTime() < period[3]['period'][1]:
            return choice(period[3]['repo'])
        elif period[4]['period'][0] <= nowTime() < period[4]['period'][1]:
            return choice(period[4]['repo'])
        else:
            return choice(period['error'])

    def _cantdo(self) -> str:
        return choice(BOT_CONFIG['cantdo']['repo'])