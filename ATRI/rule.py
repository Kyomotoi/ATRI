from nonebot.rule import Rule
from nonebot.adapters import Bot, Event


def to_bot() -> Rule:
    async def _to_bot(bot: Bot, event: Event) -> bool:
        return event.is_tome()

    return Rule(_to_bot)
