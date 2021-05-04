from nonebot.rule import Rule
from nonebot.adapters.cqhttp import GroupMessageEvent, PokeNotifyEvent

from .service import Service as sv


def is_in_service(service: str) -> Rule:
    async def _is_in_service(bot, event, state) -> bool:
        user = str(event.user_id)
        if isinstance(event, GroupMessageEvent):
            return sv.auth_service(service, user, str(event.group_id))
        else:
            return sv.auth_service(service, user, None)

    return Rule(_is_in_service)


def to_bot() -> Rule:
    async def _to_bot(bot, event, state) -> bool:
        return event.is_tome()

    return Rule(_to_bot)


def poke(bot, event: PokeNotifyEvent, state):
    if event.is_tome():
        return True
    else:
        return False
