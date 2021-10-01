import base64

# from pathlib import Path
from random import choice
from nonebot.adapters.cqhttp import MessageSegment

from ATRI.service import Service
from ATRI.rule import is_in_service
from ATRI.utils import request


LOLICON_URL = "https://api.lolicon.app/setu/v2"


class Setu(Service):
    def __init__(self):
        Service.__init__(self, "涩图", "hso!", rule=is_in_service("涩图"))

    @staticmethod
    async def random_setu() -> tuple:
        """
        随机涩图.
        """
        res = await request.get(LOLICON_URL)
        data: dict = res.json()
        temp_data: dict = data.get("data", list())
        if not temp_data:
            return "涩批爬", None

        data: dict = temp_data[0]
        title = data.get("title", "木陰のねこ")
        p_id = data.get("pid", 88124144)
        url = data["urls"].get("original", "ignore")

        setu = MessageSegment.image(url, timeout=114514)
        repo = f"Title: {title}\nPid: {p_id}"
        return repo, setu

    @staticmethod
    async def tag_setu(tag: str) -> tuple:
        """
        指定tag涩图.
        """
        url = LOLICON_URL + f"?tag={tag}"
        res = await request.get(url)
        data: dict = res.json()

        temp_data: dict = data.get("data", list())
        if not temp_data:
            return f"没有 {tag} 的涩图呢...", None

        data = temp_data[0]
        title = data.get("title", "木陰のねこ")
        p_id = data.get("pid", 88124144)
        url = data["urls"].get(
            "original",
            "https://i.pixiv.cat/img-original/img/2021/02/28/22/44/49/88124144_p0.jpg",
        )
        setu = MessageSegment.image(url, timeout=114514)
        repo = f"Title: {title}\nPid: {p_id}"
        return repo, setu

    @staticmethod
    async def scheduler() -> str:
        """
        每隔指定时间随机抽取一个群发送涩图.
        格式：
            是{tag}哦~❤
            {setu}
        """
        res = await request.get(LOLICON_URL)
        data: dict = res.json()
        temp_data: dict = data.get("data", list())
        if not temp_data:
            return ""

        tag = choice(temp_data.get("tags", ["女孩子"]))

        temp_arg = temp_data[0].get(
            "urls",
            "https://i.pixiv.cat/img-original/img/2021/02/28/22/44/49/88124144_p0.jpg",
        )
        url = temp_data[0]["urls"].get(
            "original",
            "https://i.pixiv.cat/img-original/img/2021/02/28/22/44/49/88124144_p0.jpg",
        )
        setu = MessageSegment.image(url, timeout=114514)
        repo = f"是{tag}哦~❤\n{setu}"
        return repo
