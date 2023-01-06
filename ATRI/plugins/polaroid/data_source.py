from ATRI import driver
from ATRI.service import ServiceTools
from ATRI.utils import request
from ATRI.log import log
from ATRI.exceptions import RequestError

from .image_dealer import image_dealer


TENCENT_AVATER_URL = "https://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640"
SOURCE_URL = "https://jsd.imki.moe/gh/Kyomotoi/CDN@master/project/ATRI/"


class Polaroid:
    @classmethod
    async def _request(cls, user_id: str) -> bytes:
        try:
            res = await request.get(TENCENT_AVATER_URL.format(user_id=user_id))
        except Exception:
            raise RequestError("Request failed!")
        data = res.read()  # type: ignore
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

    try:
        for i in files:
            path = POLAROID_DIR / i
            if not path.is_file():
                log.warning("插件 polaroid 缺少所需资源，装载中")
                url = SOURCE_URL + i
                data = await request.get(url)
                with open(path, "wb") as w:
                    w.write(data.read())  # type: ignore
    except Exception:
        ServiceTools("拍立得").service_controller(False)
        log.error(f"插件 polaroid 装载资源失败. 已自动禁用")

    log.success("插件 polaroid 装载资源完成")


driver().on_startup(init_source)
