import re
from typing import Tuple
from nonebot.adapters.onebot.v11 import MessageSegment

from ATRI import conf
from ATRI.utils import request
from ATRI.exceptions import RequestError

from .models import LoliconResponse, SetuInfo
from .nsfw_checker import detect_image, init_model


_LOLICON_URL = "https://api.lolicon.app/setu/v2"


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
        url = _LOLICON_URL + (f"?tag={tag}" if tag else str())
        try:
            req = await request.get(url)
        except Exception:
            raise RequestError("setu: 请求失败")

        data = LoliconResponse.parse_obj(req.json()).data[0]
        title = data.title
        pid = data.pid
        url = data.urls.original

        if conf.Setu.reverse_proxy:
            patt = "://(.*?)/"
            domain = re.findall(patt, url)[0]
            setu = url.replace(domain, conf.Setu.reverse_proxy_domain)

        setu_data = SetuInfo(title=title, pid=pid, url=url)
        setu = MessageSegment.image(
            file=url,
            timeout=114514,
        )

        return setu, setu_data

    async def detecter(self, max_size: int, disab_gif: bool) -> float:
        """图片涩值检测

        Args:
            max_size (int): 检测文件大小限制
            disab_gif (bool): 是否检测动图

        Returns:
            float: 百分比涩值
        """
        return await detect_image(self.url, max_size, disab_gif)


from ATRI import driver

driver().on_startup(init_model)
