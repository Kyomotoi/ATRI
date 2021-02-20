import datetime
from random import choice

from nonebot.rule import Rule
from nonebot.adapters.cqhttp.event import Event
from nonebot.adapters.cqhttp import GroupMessageEvent, PokeNotifyEvent

from .config import config
from .service.limit import Limit
from .service.banlist import BanSystem
from .service import Service
from .utils.list import count_list, del_list_aim
from .utils.apscheduler import scheduler, DateTrigger


def is_in_service(service: str) -> Rule:
    async def _is_in_service(bot, event, state) -> bool:
        if isinstance(event, GroupMessageEvent):
            return await Limit.auth_service(service, event.group_id)
        return await Limit.auth_service(service)
    
    return Rule(_is_in_service)


def is_in_banlist() -> Rule:
    async def _is_in_banlist(bot, event, state) -> bool:
        return BanSystem.is_in_list(str(event.get_user_id()))
    
    return Rule(_is_in_banlist)


def is_in_dormant() -> Rule:
    async def _is_in_dormant(bot, event, state) -> bool:
        return Service.is_dormant()
    
    return Rule(_is_in_dormant)


exciting_user = []
exciting_repo = [
    "歇歇8，。咱8能再快了",
    "太快惹，太快惹嗯",
    "你吼辣么快干什么！",
    "其实吧我觉得你这速度去d个vup挺适合",
    "我不接受！你太快了",
    "我有点担心，因为你太快了",
    "请稍等！您冲得太快了！"
]

def is_too_exciting(times: int, repo: bool) -> Rule:
    def del_list(user: str) -> None:
        global exciting_user
        exciting_user = del_list_aim(exciting_user, user)

    async def _is_too_exciting(bot, event, state) -> bool:
        global exciting_user
        user = event.get_user_id()
        
        if user in exciting_user:
            if repo:
                await bot.send(
                    event,
                    choice(exciting_repo)
                )
            return False
        else:
            if count_list(exciting_user, user) == times:
                delta = datetime.timedelta(
                    seconds=config["BotSelfConfig"]["session_exciting_time"])
                trigger = DateTrigger(
                    run_date=datetime.datetime.now() + delta)
                
                scheduler.add_job(
                    func=del_list,
                    trigger=trigger,
                    args=(user,),
                    misfire_grace_time=1,
                )
                
                if repo:
                    await bot.send(
                        event,
                        choice(exciting_repo)
                    )
                return False
            else:
                exciting_user.append(user)
                return True
    
    return Rule(_is_too_exciting)


def to_bot() -> Rule:
    async def _to_bot(bot, event, state) -> bool:
        return event.is_tome()
    
    return Rule(_to_bot)


def poke(bot, event: PokeNotifyEvent, state):
    if event.is_tome():
        return True
    else:
        return False
