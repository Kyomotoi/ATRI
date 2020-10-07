#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nonebot.log import logger
from nonebot.plugin import on_message
from nonebot.adapters.cqhttp import Bot, Event

from utils.utils_history import saveMessage


MessageSave = on_message()

@MessageSave.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)
    message = str(event.message)
    message_id = str(event.id)

    if group == "None":
        saveMessage(message_id, message, user)
    else:
        saveMessage(message_id, message, user, group)
    
    logger.opt(colors=True).info(f"[<yellow>{group}</yellow>]-U: (<blue>{user}</blue>) | Message: (<green>{message}</green>) Saved successfully")