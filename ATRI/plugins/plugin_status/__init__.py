#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil
import sqlite3
from pathlib import Path

from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, Event

from utils.utils_banList import banList
from utils.utils_error import errorRepo


status_info = on_command('status')

@status_info.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)

    if banList(user, group):
        msg = str(event.message).strip()
        
        if msg:
            pass
        else:
            msg0 = "States parameter:\n"
            msg0 += "- info\n"
            msg0 += "- sqlite\n"
            msg0 += "DEMO: status info"

            await status_info.finish(msg0)

        if msg == "info":
            try:
                cpu = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory().percent
                disk = psutil.disk_usage('/').percent
                inteSENT = psutil.net_io_counters().bytes_sent # type: ignore
                inteRECV = psutil.net_io_counters().bytes_recv # type: ignore
            except:
                await status_info.finish(errorRepo("读取系统状态失败"))
            
            status = "アトリは、高性能ですから！"

            if cpu > 80: # type: ignore
                status = 'ATRI感觉头有点晕...'
                if memory > 80: # type: ignore
                    status = 'ATRI感觉有点头晕并且有点累...'
            elif disk > 80: # type: ignore
                status = 'ATRI感觉身体要被塞满了...'
            
            msg0 = "ATRI status-info:\n"
            msg0 += f"* CPU: {cpu}%\n" # type: ignore
            msg0 += f"* MEM: {memory}%\n" # type: ignore
            msg0 += f"* Disk {disk}%\n" # type: ignore
            msg0 += f"* BytesSENT: {inteSENT}\n" # type: ignore
            msg0 += f"* BytesRECV: {inteRECV}\n" # type: ignore
            msg0 += status

            await status_info.finish(msg0)
        
        elif msg == "sqlite":
            con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'data_Sqlite' / 'setu' / 'normal.db') # setu-normal
            cur = con.cursor()
            cur.execute("select * from normal")
            data_normal = len(cur.fetchall())
            con.close()

            con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'data_Sqlite' / 'setu' / 'nearR18.db') # setu-nearR18
            cur = con.cursor()
            cur.execute("select * from nearR18")
            data_nearR18 = len(cur.fetchall())
            con.close()

            con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'data_Sqlite' / 'setu' / 'r18.db') # setu-r18
            cur = con.cursor()
            cur.execute("select * from r18")
            data_r18 = len(cur.fetchall())
            con.close()

            con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'data_Sqlite' / 'cloudmusic' / 'cloudmusic.db') # cloudmusic
            cur = con.cursor()
            cur.execute("select * from cloudmusic")
            data_cloudmusic = len(cur.fetchall())
            con.close()

            msg0 = "ATRI status-sqlite:\n"
            msg0 += "Setu:\n"
            msg0 += f"│ │ └ normal: {data_normal}\n"
            msg0 += f"│ └ nearR18: {data_nearR18}\n"
            msg0 += f"└ R18: {data_r18}\n"
            msg0 += "CloudMusic:\n"
            msg0 += f"└ Message: {data_cloudmusic}"

            await status_info.finish(msg0)