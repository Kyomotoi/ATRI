import json
import socket
import string
import zipfile
from random import sample
from pathlib import Path

from nonebot.permission import SUPERUSER

from ATRI.service import Service
from ATRI.utils import request
from ATRI.rule import is_in_service
from ATRI.exceptions import WriteFileError
from ATRI.log import log


CONSOLE_DIR = Path(".") / "data" / "plugins" / "console"
CONSOLE_DIR.mkdir(parents=True, exist_ok=True)


class Console(Service):
    def __init__(self):
        Service.__init__(
            self,
            "控制台",
            "前端管理页面",
            True,
            is_in_service("控制台"),
            main_cmd="/con",
            permission=SUPERUSER,
        )

    @staticmethod
    async def get_host_ip(is_pub: bool):
        if is_pub:
            data = await request.get("https://ifconfig.me/ip")
            return data.text

        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
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
        df = CONSOLE_DIR / "data.json"
        if not df.is_file():
            try:
                with open(df, "w", encoding="utf-8") as w:
                    w.write(json.dumps(dict()))
            except Exception:
                raise WriteFileError("Writing file: " + str(df) + " failed!")

        base_data: dict = json.loads(df.read_bytes())
        data = base_data.get("data", None)
        if not data:
            return {"data": None}
        return data


FRONTEND_DIR = CONSOLE_DIR / "frontend"
FRONTEND_DIR.mkdir(parents=True, exist_ok=True)
CONSOLE_RESOURCE_URL = (
    "https://jsd.imki.moe/gh/kyomotoi/Project-ATRI-Console@main/archive/dist.zip"
)


async def init_resource():
    log.info("控制台初始化中...")

    try:
        resp = await request.get(CONSOLE_RESOURCE_URL)
    except Exception:
        log.error("控制台资源装载失败, 将无法访问管理界面")
        return

    file_path = CONSOLE_DIR / "dist.zip"
    with open(file_path, "wb") as w:
        w.write(resp.read())

    with zipfile.ZipFile(file_path, "r") as zr:
        zr.extractall(FRONTEND_DIR)

    log.success("控制台初始化完成")
