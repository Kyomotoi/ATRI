import asyncio
from nonebot.adapters.onebot.v11 import Bot, MessageSegment

from ATRI import conf
from ATRI.utils import request
from .nsfw_checker import detect_image, init_model


LOLICON_URL = "https://api.lolicon.app/setu/v2"
DEFAULT_SETU = (
    "https://i.pixiv.cat/img-original/img/2021/02/28/22/44/49/88124144_p0.jpg"
)


class Setu:
    @staticmethod
    def _use_proxy(url: str) -> str:
        if conf.Setu.reverse_proxy:
            return url.replace("i.pixiv.cat", conf.Setu.reverse_proxy_domain)
        else:
            return url

    @classmethod
    async def random_setu(cls) -> tuple:
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
        url: str = data["urls"].get("original", "ignore")

        setu = MessageSegment.image(cls._use_proxy(url), timeout=114514)
        repo = f"Title: {title}\nPid: {p_id}"
        return repo, setu

    @classmethod
    async def tag_setu(cls, tag: str) -> tuple:
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
            cls._use_proxy(DEFAULT_SETU),
        )
        setu = MessageSegment.image(url, timeout=114514)
        repo = f"Title: {title}\nPid: {p_id}"
        return repo, setu

    @staticmethod
    async def detecter(url: str, file_size: int) -> float:
        """
        涩值检测.
        """
        data = await detect_image(url, file_size)
        return data

    @staticmethod
    async def async_recall(bot: Bot, event_id):
        await asyncio.sleep(30)
        await bot.delete_msg(message_id=event_id)


from ATRI import driver

driver().on_startup(init_model)
