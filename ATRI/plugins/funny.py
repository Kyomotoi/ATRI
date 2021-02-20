from pathlib import Path
from random import choice, randint

from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.plugin import on_command, on_message

from ATRI.rule import (
    is_in_banlist,
    is_in_dormant,
    is_in_service
)


__plugin_name__ = "laugh"

get_laugh = on_command(
    "来句笑话",
    rule=is_in_banlist() & is_in_dormant()
    & is_in_service(__plugin_name__)
)

@get_laugh.handle()
async def _get_laugh(bot: Bot, event: MessageEvent) -> None:
    user_name = event.sender.nickname
    laugh_list = []
    
    FILE = Path('.') / 'ATRI' / 'data' / 'database' / 'funny' / 'laugh.txt'
    with open(FILE, 'r', encoding='utf-8') as r:
        for line in r:
            laugh_list.append(line.strip('\n'))
    
    result = choice(laugh_list)
    await get_laugh.finish(result.replace("%name", user_name))


__plugin_name__ = "wty"

me_to_you = on_message(
    rule=is_in_banlist() & is_in_dormant() & is_in_service(__plugin_name__)
)

@me_to_you.handle()
async def _me_to_you(bot: Bot, event: MessageEvent) -> None:
    if randint(0, 5) == 5:
        msg = str(event.message)
        if "我" in msg and "CQ" not in msg:
            await me_to_you.finish(msg.replace("我", "你"))
