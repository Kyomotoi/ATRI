from nonebot.rule import Rule
from nonebot.adapters.cqhttp import GroupMessageEvent, PokeNotifyEvent

from .config import config
from .service import Service as sv


def is_in_service(service: str) -> Rule:
    async def _is_in_service(bot, event, state) -> bool:
        if isinstance(event, GroupMessageEvent):
            return sv.auth_service(service, event.group_id)
        else:
            return sv.auth_service(service, None)
    
    return Rule(_is_in_service)


def is_block() -> Rule:
    async def _is_in_banlist(bot, event, state) -> bool:
        return sv.BlockSystem.auth_user(int(event.get_user_id()))
    
    return Rule(_is_in_banlist)


def is_in_dormant() -> Rule:
    async def _is_in_dormant(bot, event, state) -> bool:
        return sv.Dormant.is_dormant()
    
    return Rule(_is_in_dormant)


def to_bot() -> Rule:
    async def _to_bot(bot, event, state) -> bool:
        return event.is_tome()
    
    return Rule(_to_bot)


def poke(bot, event: PokeNotifyEvent, state):
    if event.is_tome():
        return True
    else:
        return False
