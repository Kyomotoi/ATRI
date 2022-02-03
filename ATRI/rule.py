from nonebot.rule import Rule
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent

from .service import ServiceTools


def is_in_service(service: str) -> Rule:
    async def _is_in_service(bot: Bot, event: Event) -> bool:
        result = ServiceTools().auth_service(service)
        if not result:
            return False

        if isinstance(event, PrivateMessageEvent):
            user_id = event.get_user_id()
            result = ServiceTools().auth_service(service, user_id)
            return result
        elif isinstance(event, GroupMessageEvent):
            user_id = event.get_user_id()
            group_id = str(event.group_id)
            result = ServiceTools().auth_service(service, user_id, group_id)
            return result
        else:
            return True

    return Rule(_is_in_service)


def to_bot() -> Rule:
    async def _to_bot(bot: Bot, event: Event) -> bool:
        return event.is_tome()

    return Rule(_to_bot)
