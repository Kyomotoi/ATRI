from re import T
from nonebot.rule import Rule
from nonebot.typing import Bot, Event

from ATRI.service import Service


def isInService(service: str) -> Rule:
    async def _isInService(bot: Bot, event: Event, state: dict) -> bool:
        return Service().Switch().auth_service(service, event.group_id)

    return Rule(_isInService)


def isInBanList() -> Rule:
    async def _isInBanList(bot: Bot, event: Event, state: dict) -> bool:
        return Service().BanList().is_in_list(event.user_id)

    return Rule(_isInBanList)


def isInDormant() -> Rule:
    async def _isInDormant(bot: Bot, event: Event, state: dict) -> bool:
        return Service().Dormant().is_sleep()

    return Rule(_isInDormant)


def toGroup() -> Rule:
    async def _toGroup(bot: Bot, event: Event, state: dict) -> bool:
        return bool(event.group_id)

    return Rule(_toGroup)


def toPrivate() -> Rule:
    async def _toPrivate(bot: Bot, event: Event, state: dict) -> bool:
        return not bool(event.group_id)

    return Rule(_toPrivate)

def toBot() -> Rule:
    async def _toBot(bot: Bot, event: Event, state: dict) -> bool:
        return bool(event.to_me)
    
    return Rule(_toBot)
