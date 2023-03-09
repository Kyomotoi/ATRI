import json
import socket
import string
import zipfile
import hashlib
from pathlib import Path
from random import sample
from typing import Optional
from datetime import datetime, timedelta

from ATRI.utils import request, FileDealer
from ATRI.log import log

from .models import AuthData


CONSOLE_DIR = Path(".") / "data" / "plugins" / "console"
CONSOLE_DIR.mkdir(parents=True, exist_ok=True)


class AuthDealer:
    AUTH_FILE_PATH = CONSOLE_DIR / "data.json"

    def __init__(self):
        self.token = str().join(sample(string.ascii_letters + string.digits, 20))

    def get_token(self):
        return self.token

    def get_md5(self):
        hl = hashlib.md5()
        hl.update(self.token.encode(encoding="utf-8"))
        return hl.hexdigest()

    async def store(self) -> AuthData:
        dead_time = (datetime.now() + timedelta(minutes=15)).timestamp()
        data = AuthData(token=self.token, md5=self.get_md5(), dead_time=int(dead_time))
        await FileDealer(self.AUTH_FILE_PATH).write(json.dumps(data.dict()))
        return data

    @classmethod
    def get(cls) -> Optional[AuthData]:
        return (
            AuthData.parse_file(cls.AUTH_FILE_PATH)
            if cls.AUTH_FILE_PATH.is_file()
            and json.loads(cls.AUTH_FILE_PATH.read_bytes())
            else None
        )

    @classmethod
    async def clear(cls):
        await FileDealer(cls.AUTH_FILE_PATH).write(json.dumps(dict()))


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


# FRONTEND_DIR = CONSOLE_DIR / "frontend"
# FRONTEND_DIR.mkdir(parents=True, exist_ok=True)
# __CONSOLE_RESOURCE_URL = (
#     "https://guc.imki.moe/kyomotoi/Project-ATRI-Console/main/archive/dist.zip"
# )


# async def init_resource():
#     log.info("控制台初始化中...")

#     try:
#         resp = await request.get(__CONSOLE_RESOURCE_URL)
#     except Exception:
#         log.error("控制台资源装载失败, 将无法访问管理界面")
#         return

#     file_path = CONSOLE_DIR / "dist.zip"
#     with open(file_path, "wb") as w:
#         w.write(resp.read())

#     with zipfile.ZipFile(file_path, "r") as zr:
#         zr.extractall(FRONTEND_DIR)

#     log.success("控制台初始化完成")
