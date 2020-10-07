#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.permission import GROUP_ADMIN, GROUP_OWNER, SUPERUSER

from utils.utils_banList import banList
from utils.utils_switch import controlSwitch

import ATRI


master = ATRI.config_SUPERUSERS


switch = on_command('switch', permission=(SUPERUSER|GROUP_OWNER|GROUP_ADMIN))

@switch.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)

    if banList(user, group):
        func = str(event.message).strip()
        
        if func:
            pass
        else:
            msg0 = "-==ATRI Switch Control System==-\n"
            msg0 += "┌Usage: switch on/off-{service}\n"
            msg0 += "├For SUPERUSER:\n"
            msg0 += "│  └Usage: switch all-on/off-{service}\n"
            msg0 += "└Service:\n"
            msg0 += "    ├anime-setu\n"
            msg0 += "    ├anime-pic-search\n"
            msg0 += "    └anime-vid-search\n"

            await switch.finish(msg0)
        
        funct = re.findall(r"[on|off]-(.*)", func)
        print(func, funct)

        print(type(master[0]), type(user))
        
        if "all-on" in func:
            if int(user) in master:
                await switch.finish(controlSwitch(funct[0], True))

            else:
                await switch.finish("You don't have enough permissions do THIS!")
        
        elif "all-off" in func:
            if int(user) in master:
                await switch.finish(controlSwitch(funct[0], False))

            else:
                await switch.finish("You don't have enough permissions do THIS!")
        
        elif "on" in func:
            await switch.finish(controlSwitch(funct[0], True, group))
        
        elif "off" in func:
            await switch.finish(controlSwitch(funct[0], False, group))

        else:
            await switch.finish("请检查拼写是否正确嗷~~！")