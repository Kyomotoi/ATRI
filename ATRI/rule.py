import datetime
from random import choice

from nonebot.adapters import Event
from nonebot.rule import Rule
from nonebot.adapters.cqhttp import GroupMessageEvent

from .service.switch import Switch
from .service.banlist import BanList
from .service.dormant import Dormant
from .apscheduler import scheduler, DateTrigger
from .config import config
from .utils import count_list, del_list_aim


warting_list = []
fast_user_list = []


def is_in_service(service: str) -> Rule:
    async def _is_in_service(bot, event, state) -> bool:
        if isinstance(event, GroupMessageEvent):
            return await Switch.auth_service(service, event.group_id)
        return await Switch.auth_service(service)

    return Rule(_is_in_service)


def is_in_ban_list() -> Rule:
    async def _is_in_ban_list(bot, event, state) -> bool:
        return BanList.is_in_list(event.get_user_id())

    return Rule(_is_in_ban_list)


def is_in_dormant() -> Rule:
    async def _is_in_dormant(bot, event, state) -> bool:
        return Dormant.is_sleep()

    return Rule(_is_in_dormant)

def is_max_times(max_times: int, time_day: int,
                 time_hour: int, time_min: int) -> Rule:
    async def _is_max_times(bot, event: Event, state) -> bool:
        global warting_list
        user = event.get_user_id()
        if user in warting_list:
            return False
        
        
        
        
        return True
    
    return Rule(_is_max_times)


def is_too_fast(times: int, _type: str) -> Rule:
    def remove_list(user: str) -> None:
        global fast_user_list
        fast_user_list = del_list_aim(fast_user_list, user)
    
    async def _is_too_fast(bot, event: Event, state) -> bool:
        global fast_user_list
        user = event.get_user_id()

        if user in fast_user_list:
            await bot.send(
                event, choice(config['bot']['session_waiting_repo']))
            return False
        else:
            if count_list(fast_user_list, user) == times:
                delta = datetime.timedelta(
                    seconds=config['bot']['session_waiting_time'])
                trigger = DateTrigger(
                    run_date=datetime.datetime.now() + delta)
                
                scheduler.add_job(
                    func=remove_list,
                    trigger=trigger,
                    args=(user,),
                    misfire_grace_time=1,
                )

                await bot.send(
                    event, choice(config['bot']['session_waiting_repo']))
                return False
            else:
                fast_user_list.append(user)
                return True
    
    return Rule(_is_too_fast)


def to_bot() -> Rule:
    async def _to_bot(bot, event: Event, state) -> bool:
        return event.is_tome()
    
    return Rule(_to_bot)


def poke() -> Rule:
    async def _poke(bot, event, state) -> bool:
        return True if event.is_tome() else False
    
    return Rule(_poke)
