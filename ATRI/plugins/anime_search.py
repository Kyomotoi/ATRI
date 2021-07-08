import re
from aiohttp import FormData
from random import choice

from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from ATRI.service import Service
from ATRI.rule import is_in_service
from ATRI.utils import request, UbuntuPaste, Translate
from ATRI.utils.limit import FreqLimiter
from ATRI.exceptions import RequestError


URL = "https://trace.moe/api/search?url="
_anime_flmt = FreqLimiter(10)
_anime_flmt_notice = choice(["慢...慢一..点❤", "冷静1下", "歇会歇会~~"])


__doc__ = """
通过一张图片搜索你需要的番！据说里*也可以
"""


class Anime(Service):
    def __init__(self):
        Service.__init__(self, "以图搜番", __doc__, rule=is_in_service("以图搜番"))

    @staticmethod
    async def _request(url: str) -> dict:
        aim = URL + url
        try:
            res = await request.get(aim)
        except RequestError:
            raise RequestError("Request failed!")
        result = await res.json()
        return result

    @classmethod
    async def search(cls, url: str) -> str:
        data = await cls._request(url)
        data = data["docs"]

        d = dict()
        for i in range(len(data)):
            if data[i]["title_chinese"] in d.keys():
                d[data[i]["title_chinese"]][0] += data[i]["similarity"]
            else:
                m = data[i]["at"] / 60
                s = data[i]["at"] % 60

                if not data[i]["episode"]:
                    n = 1
                else:
                    n = data[i]["episode"]

                d[Translate(data[i]["title_chinese"]).to_simple()] = [
                    data[i]["similarity"],
                    f"第{n}集",
                    f"{int(m)}分{int(s)}秒处",
                ]

        result = sorted(d.items(), key=lambda x: x[1], reverse=True)
        t = 0
        msg0 = str()
        for i in result:
            t += 1
            s = "%.2f%%" % (i[1][0] * 100)
            msg0 = msg0 + (
                "\n——————————\n"
                f"({t}) Similarity: {s}\n"
                f"Name: {i[0]}\n"
                f"Time: {i[1][1]} {i[1][2]}"
            )

        if len(result) == 2:
            return msg0
        else:
            data = FormData()
            data.add_field("poster", "ATRI running log")
            data.add_field("syntax", "text")
            data.add_field("expiration", "day")
            data.add_field("content", msg0)

            repo = f"详细请移步此处~\n{await UbuntuPaste(data).paste()}"
            return repo


anime_search = Anime().on_command("以图搜番", "发送一张图以搜索可能的番剧")


@anime_search.args_parser  # type: ignore
async def _get_anime(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了", "不搜了", "取消"]
    if msg in quit_list:
        await anime_search.finish("好吧...")
    if not msg:
        await anime_search.reject("图呢？")
    else:
        state["anime"] = msg


@anime_search.handle()
async def _ready_sear(bot: Bot, event: MessageEvent, state: T_State):
    user_id = event.get_user_id()
    if not _anime_flmt.check(user_id):
        await anime_search.finish(_anime_flmt_notice)

    msg = str(event.message).strip()
    if msg:
        state["anime"] = msg


@anime_search.got("anime", "图呢？")
async def _deal_sear(bot: Bot, event: MessageEvent, state: T_State):
    user_id = event.get_user_id()
    msg = state["anime"]
    img = re.findall(r"url=(.*?)]", msg)
    if not img:
        await anime_search.reject("请发送图片而不是其它东西！！")

    a = await Anime().search(img[0])
    result = f"> {MessageSegment.at(user_id)}\n" + a
    _anime_flmt.start_cd(user_id)
    await anime_search.finish(Message(result))
