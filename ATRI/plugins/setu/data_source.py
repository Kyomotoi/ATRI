import base64

# from pathlib import Path
from random import choice
from nonebot.adapters.cqhttp import MessageSegment

from ATRI.service import Service
from ATRI.rule import is_in_service
from ATRI.utils import request


LOLICON_URL = "https://api.lolicon.app/setu/v2"
SCHEDULER_FORMAT = """
是{tag}哦~❤
{setu}
"""


class Setu(Service):
    def __init__(self):
        Service.__init__(self, "涩图", "hso!", rule=is_in_service("涩图"))

    @staticmethod
    async def random_setu() -> tuple:
        """
        随机涩图.
        """
        res = await request.get(LOLICON_URL)
        data: dict = await res.json()
        temp_data: dict = data.get("data", list())[0]

        title = temp_data.get("title", "木陰のねこ")
        p_id = temp_data.get("pid", 88124144)
        url = temp_data["urls"].get("original", "ignore")

        setu = MessageSegment.image(url, timeout=114514)
        return setu, title, p_id

    @staticmethod
    async def tag_setu(tag: str) -> tuple:
        """
        指定tag涩图.
        """
        url = LOLICON_URL + f"?tag={tag}"
        res = await request.get(url)
        data: dict = await res.json()

        try :
            temp_data: dict = data.get("data", list())[0]
            is_ok = True
            title = temp_data.get("title", "木陰のねこ")
            p_id = temp_data.get("pid", 88124144)
            url = temp_data["urls"].get("original", "ignore")
            setu = MessageSegment.image(url, timeout=114514)
        except :
            setu,title,p_id,is_ok = None,None,None,False
        return setu, title, p_id, is_ok

    @staticmethod
    async def scheduler() -> str:
        """
        每隔指定时间随机抽取一个群发送涩图.
        格式：
            是{tag}哦~❤
            {setu}
        """
        res = await request.get(LOLICON_URL)
        data: dict = await res.json()
        temp_data: dict = data.get("data", list())[0]

        tag = choice(temp_data.get("tags", ["女孩子"]))

        url = temp_data["urls"].get("original", "ignore")
        setu = MessageSegment.image(url, timeout=114514)
        repo = SCHEDULER_FORMAT.format(tag=tag, setu=setu)
        return repo
