#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/10/11 14:40:55
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import psutil
import sqlite3
from pathlib import Path
from random import choice

from nonebot.plugin import on_command
from nonebot.typing import Bot, Event
from nonebot.permission import SUPERUSER

from ATRI.utils.utils_error import errorRepo
from ATRI.utils.utils_rule import check_banlist

# States parameter:
# ├info
# └sqlite
# * DEMO: status info
status_info = on_command('/status', rule=check_banlist())


@status_info.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    msg = str(event.message).strip()

    if not msg:
        await status_info.finish("请查看文档获取帮助（")

    if msg == "info":
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            inteSENT = psutil.net_io_counters().bytes_sent  # type: ignore
            inteRECV = psutil.net_io_counters().bytes_recv  # type: ignore
        except:
            await status_info.finish(errorRepo("读取系统状态失败"))

        status = "アトリは、高性能ですから！"

        if cpu > 80:  # type: ignore
            status = 'ATRI感觉头有点晕...'
            if memory > 80:  # type: ignore
                status = 'ATRI感觉有点头晕并且有点累...'
        elif disk > 80:  # type: ignore
            status = 'ATRI感觉身体要被塞满了...'

        msg0 = "ATRI status-info:\n"
        msg0 += f"* CPU: {cpu}%\n"  # type: ignore
        msg0 += f"* MEM: {memory}%\n"  # type: ignore
        msg0 += f"* Disk {disk}%\n"  # type: ignore
        msg0 += f"* BytesSENT: {inteSENT}\n"  # type: ignore
        msg0 += f"* BytesRECV: {inteRECV}\n"  # type: ignore
        msg0 += status

        await status_info.finish(msg0)

    elif msg == "sqlite":
        con = sqlite3.connect(
            Path('.') / 'ATRI' / 'data' / 'data_Sqlite' / 'setu' /
            'normal.db')  # setu-normal
        cur = con.cursor()
        cur.execute("select * from normal")
        data_normal = len(cur.fetchall())
        con.close()

        con = sqlite3.connect(
            Path('.') / 'ATRI' / 'data' / 'data_Sqlite' / 'setu' /
            'nearR18.db')  # setu-nearR18
        cur = con.cursor()
        cur.execute("select * from nearR18")
        data_nearR18 = len(cur.fetchall())
        con.close()

        con = sqlite3.connect(
            Path('.') / 'ATRI' / 'data' / 'data_Sqlite' / 'setu' /
            'r18.db')  # setu-r18
        cur = con.cursor()
        cur.execute("select * from r18")
        data_r18 = len(cur.fetchall())
        con.close()

        msg0 = "ATRI status-sqlite:\n"
        msg0 += "Setu:\n"
        msg0 += f"├normal: {data_normal}\n"
        msg0 += f"├nearR18: {data_nearR18}\n"
        msg0 += f"└R18: {data_r18}"

        await status_info.finish(msg0)


ping = on_command('/ping', permission=SUPERUSER)


@ping.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    await ping.finish(choice(["I'm fine.", "啪！"]))
