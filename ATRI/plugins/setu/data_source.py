from typing import Tuple
from nonebot.adapters.onebot.v11 import MessageSegment

from ATRI import conf
from ATRI.utils import request
from ATRI.exceptions import RequestError

from .models import SetuInfo
from .nsfw_checker import detect_image, init_model


__LOLICON_URL = "https://api.lolicon.app/setu/v2"


class Setu:
    def __init__(self, url: str):
        self.url = url

    @classmethod
    async def new(cls, tag: str = str()) -> Tuple[MessageSegment, SetuInfo]:
        """new 一个涩图

        Args:
            tag (str, optional): 附加 tag, 默认无

        Raises:
            RequestError: 涩图请求失败

        Returns:
            Tuple[MessageSegment, dict]: 涩图本体, 涩图信息
        """
        url = __LOLICON_URL
        if tag:
            url = __LOLICON_URL + f"?tag={tag}"
        try:
            req = await request.get(url)
        except Exception:
            raise RequestError("setu: 请求失败")

        data = req.json()
        cache_data = data.get("data")
        if not cache_data:
            raise RequestError("今天不可以涩")

        data = cache_data[0]
        title = data["title"]
        pid = data["pid"]
        setu = data["urls"].get("original", "ignore")

        if conf.Setu.reverse_proxy:
            setu = MessageSegment.image(
                file=setu.replace("i.pixiv.cat", conf.Setu.reverse_proxy_domain),
                timeout=114514,
            )

        setu_data = SetuInfo(title=title, pid=pid)

        return setu, setu_data

    async def detecter(self, max_size: int) -> float:
        """图片涩值检测

        Args:
            max_size (int): 检测文件大小限制

        Returns:
            float: 百分比涩值
        """
        return await detect_image(self.url, max_size)


from ATRI import driver

driver().on_startup(init_model)
