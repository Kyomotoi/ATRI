import os
import time
import json
import psutil
import socket
import string
from pathlib import Path
from random import sample
from datetime import datetime

from ATRI.service import Service
from ATRI.log import logger as log
from ATRI.rule import is_in_service
from ATRI.utils import request
from ATRI.exceptions import GetStatusError, WriteError
from .models import PlatfromRuntimeInfo, BotRuntimeInfo


STATUS_DIR = Path(".") / "data" / "database" / "status"
STATUS_DIR.mkdir(exist_ok=True)

_status_msg = """
> Status Overview

[CPU: {p_cpu}% of {b_cpu}]
[Memory: {p_mem}% of {b_mem}]
[Disk usage: {p_disk}%]

[Net sent: {inteSENT}MB]
[Net recv: {inteRECV}MB]

[Bot runtime: {bot_time}]
[Platform runtime: {boot_time}]
{msg}
""".strip()


class Status(Service):
    def __init__(self):
        Service.__init__(self, "状态", "检查自身状态", rule=is_in_service("状态"))

    @staticmethod
    def ping() -> str:
        return "I'm fine."

    @staticmethod
    def get_status(is_for_fn: bool = False) -> tuple:
        data_p = Path(".") / "data"

        try:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            disk = psutil.disk_usage("/").percent
            inteSENT = psutil.net_io_counters().bytes_sent / 1000000  # type: ignore
            inteRECV = psutil.net_io_counters().bytes_recv / 1000000  # type: ignore

            process = psutil.Process(os.getpid())
            b_cpu = process.cpu_percent(interval=1)
            b_mem = process.memory_percent(memtype="rss")

            now = time.time()
            boot = psutil.boot_time()
            b = process.create_time()
            boot_time = str(
                datetime.utcfromtimestamp(now).replace(microsecond=0)
                - datetime.utcfromtimestamp(boot).replace(microsecond=0)
            )
            bot_time = str(
                datetime.utcfromtimestamp(now).replace(microsecond=0)
                - datetime.utcfromtimestamp(b).replace(microsecond=0)
            )
        except GetStatusError:
            raise GetStatusError("Failed to get status.")

        msg = "アトリは、高性能ですから！"
        if cpu > 90:  # type: ignore
            msg = "咱感觉有些头晕..."
            is_ok = False
            if mem > 90:
                msg = "咱感觉有点头晕并且有点累..."
                is_ok = False
        elif mem > 90:
            msg = "咱感觉有点累..."
            is_ok = False
        elif disk > 90:
            msg = "咱感觉身体要被塞满了..."
            is_ok = False
        else:
            is_ok = True

        if is_for_fn:
            return (
                PlatfromRuntimeInfo(
                    stat_msg=msg,
                    cpu_percent=str(cpu),
                    mem_percent=mem,
                    disk_percent=str(disk),
                    inte_send=str(inteSENT),
                    inte_recv=str(inteRECV),
                    boot_time=boot_time,
                ).dict(),
                BotRuntimeInfo(
                    cpu_percent=str(b_cpu),
                    mem_percent=str(b_mem),
                    bot_run_time=bot_time,
                ).dict(),
            )

        msg0 = _status_msg.format(
            p_cpu=cpu,
            p_mem=mem,
            p_disk=disk,
            b_cpu=f"{b_cpu}%",
            b_mem="%.1f%%" % b_mem,
            inteSENT=inteSENT,
            inteRECV=inteRECV,
            bot_time=bot_time,
            boot_time=boot_time,
            msg=msg,
        )

        return msg0, is_ok

    @staticmethod
    async def get_host_ip(is_pub: bool):
        if is_pub:
            data = await request.get("https://ifconfig.me/ip")
            return data.text

        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            return ip
        finally:
            if s:
                s.close()

    @staticmethod
    def get_random_str(k: int) -> str:
        return "".join(sample(string.ascii_letters + string.digits, k))

    @staticmethod
    def get_auth_info() -> dict:
        df = STATUS_DIR / "data.json"
        if not df.is_file():
            try:
                with open(df, "w", encoding="utf-8") as w:
                    w.write(json.dumps({}))
            except WriteError:
                raise WriteError("Writing file: " + str(df) + " failed!")

        base_data: dict = json.loads(df.read_bytes())
        data = base_data.get("data", None)
        if not data:
            return {"data": None}
        return data
