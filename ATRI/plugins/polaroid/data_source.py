import asyncio

from ATRI.service import Service
from ATRI.rule import is_in_service
from ATRI.utils import request
from ATRI.log import logger as log
from ATRI.exceptions import RequestError, WriteError
from .image_dealer import image_dealer


TENCENT_AVATER_URL = "https://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640"
SOURCE_URL = "https://cdn.jsdelivr.net/gh/Kyomotoi/CDN@master/project/ATRI/"


class Polaroid(Service):
    def __init__(self):
        Service.__init__(self, "拍立得", "根据头像生成拍立得风格照片！", rule=is_in_service("拍立得"))

    @classmethod
    async def _request(cls, user_id: str) -> bytes:
        try:
            res = await request.get(TENCENT_AVATER_URL.format(user_id=user_id))
        except RequestError:
            raise RequestError("Request failed!")
        data = res.read()
        return data

    @classmethod
    async def generate(cls, user_id: str):
        await init_source()

        user_avater = await cls._request(user_id)

        result = image_dealer(user_avater, user_id)
        return f"file:///{result}"


from .image_dealer import TEMP_PATH, POLAROID_DIR


async def init_source():
    files = ["frame-0.PNG", "frame-1.PNG", "font-0.ttf"]

    for i in files:
        path = POLAROID_DIR / i
        if not path.is_file():
            log.warning("插件 polaroid 缺少所需资源，装载中")

            url = SOURCE_URL + i
            data = await request.get(url)
            try:
                with open(path, "wb") as w:
                    w.write(data.read())
                log.info("所需资源装载完成")
            except WriteError:
                raise WriteError("装载资源失败")


loop = asyncio.get_event_loop()
loop.create_task(init_source())
