import os
import json
import string
import aiosqlite
from aiosqlite.core import Connection
from pathlib import Path
from random import sample, choice
from aiohttp import ClientSession
from nonebot.adapters.cqhttp.message import MessageSegment, Message

from ATRI.log import logger as log
from ATRI.config import NsfwCheck
from ATRI.exceptions import RequestError, WriteError
from ATRI.utils.request import get_bytes
from ATRI.utils.img import compress_image


TEMP_DIR: Path = Path(".") / "ATRI" / "data" / "temp" / "setu"
SETU_DIR = Path(".") / "ATRI" / "data" / "database" / "setu"
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(SETU_DIR, exist_ok=True)
NSFW_URL = f"http://{NsfwCheck.host}:{NsfwCheck.port}/?url="
SIZE_REDUCE: bool = True


class Hso:
    @staticmethod
    async def nsfw_check(url: str) -> float:
        url = NSFW_URL + url
        try:
            data = json.loads(await get_bytes(url))
        except RequestError:
            raise RequestError("Request failed!")
        return round(data["score"], 4)

    @staticmethod
    async def _comp_setu(url: str) -> str:
        temp_id = "".join(sample(string.ascii_letters + string.digits, 8))
        file = TEMP_DIR / f"{temp_id}.png"

        try:
            async with ClientSession() as session:
                async with session.get(url) as r:
                    data = await r.read()
        except RequestError:
            raise RequestError("Request img failed!")

        try:
            with open(file, "wb") as r:
                r.write(data)
        except WriteError:
            raise WriteError("Writing img failed!")

        return compress_image(os.path.abspath(file))

    @classmethod
    async def setu(cls, data: dict) -> str:
        pid = data["pid"]
        title = data["title"]
        if SIZE_REDUCE:
            img = MessageSegment.image(
                "file:///" + await cls._comp_setu(data["url"]), proxy=False
            )
        else:
            img = MessageSegment.image(data["url"], proxy=False)

        msg = f"Pid: {pid}\n" f"Title: {title}\n" f"{img}"
        return msg

    @classmethod
    async def acc_setu(cls, d: list) -> str:
        data: dict = choice(d)

        for i in data["tags"]:
            if i["name"] == "R-18":
                return "太涩了不方便发w"

        pid = data["id"]
        title = data["title"]
        try:
            pic = data["meta_single_page"]["original_image_url"].replace(
                "pximg.net", "pixiv.cat"
            )
        except Exception:
            pic = choice(data["meta_pages"])["original"]["image_urls"].replace(
                "pximg.net", "pixiv.cat"
            )
        if SIZE_REDUCE:
            img = MessageSegment.image(
                "file:///" + await cls._comp_setu(pic), proxy=False
            )
        else:
            img = MessageSegment.image(pic, proxy=False)

        msg = f"Pid: {pid}\n" f"Title: {title}\n" f"{img}"
        return msg


class SetuData:
    SETU_DATA = SETU_DIR / "setu.db"

    @classmethod
    async def _check_database(cls) -> bool:
        if not cls.SETU_DATA.exists():
            log.warning(f"未发现数据库\n-> {cls.SETU_DATA}\n将开始创建")
            async with aiosqlite.connect(cls.SETU_DATA) as db:
                cur = await db.cursor()
                await cur.execute(
                    """
                    CREATE TABLE setu(
                        pid PID, title TITLE, tags TAGS,
                        user_id USER_ID, user_name USER_NAME,
                        user_account USER_ACCOUNT, url URL,
                        UNIQUE(
                            pid, title, tags, user_id,
                            user_name, user_account, url
                        )
                    );
                    """
                )
                await db.commit()
            log.warning(f"...创建数据库\n-> {cls.SETU_DATA}\n完成！")
            return True
        return True

    @classmethod
    async def add_data(cls, d: dict) -> None:
        data = (
            d["pid"],
            d["title"],
            d["tags"],
            d["user_id"],
            d["user_name"],
            d["user_account"],
            d["url"],
        )

        check = await cls._check_database()
        if check:
            async with aiosqlite.connect(cls.SETU_DATA) as db:
                await db.execute(
                    """
                    INSERT INTO setu(
                        pid, title, tags, user_id,
                        user_name, user_account, url
                    ) VALUES(
                        ?, ?, ?, ?, ?, ?, ?
                    );
                    """,
                    data,
                )
                await db.commit()

    @classmethod
    async def del_data(cls, pid: int) -> None:
        if not isinstance(pid, int):  # 防注入
            raise ValueError("Please provide int.")

        check = await cls._check_database()
        if check:
            async with aiosqlite.connect(cls.SETU_DATA) as db:
                await db.execute(f"DELETE FROM setu WHERE pid = {str(pid)};")
                await db.commit()

    @classmethod
    async def count(cls):
        check = await cls._check_database()
        if check:
            async with aiosqlite.connect(cls.SETU_DATA) as db:
                async with db.execute("SELECT * FROM setu") as cursor:
                    return len(await cursor.fetchall())  # type: ignore

    @classmethod
    async def get_setu(cls):
        check = await cls._check_database()
        if check:
            async with aiosqlite.connect(cls.SETU_DATA) as db:
                async with db.execute(
                    "SELECT * FROM setu ORDER BY RANDOM() limit 1;"
                ) as cursor:
                    return await cursor.fetchall()
