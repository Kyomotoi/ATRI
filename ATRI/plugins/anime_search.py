from random import choice

from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.adapters.onebot.v11.helpers import extract_image_urls, Cooldown

from ATRI.service import Service
from ATRI.utils import request, Translate
from ATRI.exceptions import RequestError


URL = "https://api.trace.moe/search?anilistInfo=true"
_anime_flmt_notice = choice(["慢...慢一..点❤", "冷静1下", "歇会歇会~~"])


class Anime:
    def __init__(self, img: str):
        self.img = img

    async def _request(self, url: str) -> dict:
        try:
            resp = await request.get(url)
            image_bytes = resp.read()
            res = await request.post(
                URL, data=image_bytes, headers={"Content-Type": "image/jpeg"}
            )
        except Exception:
            raise RequestError("Request failed!")
        result = res.json()
        return result

    async def do_search(self) -> str:
        data = await self._request(self.img)
        try:
            data = data["result"]
        except Exception:
            return "没有相似的结果呢..."

        d = dict()
        for i in range(3):
            if data[i]["anilist"]["title"]["native"] in d.keys():
                d[data[i]["anilist"]["title"]["native"]][0] += data[i]["similarity"]
            else:
                from_m = data[i]["from"] / 60
                from_s = data[i]["from"] % 60

                to_m = data[i]["to"] / 60
                to_s = data[i]["to"] % 60

                if not data[i]["episode"]:
                    n = 1
                else:
                    n = data[i]["episode"]

                d[Translate(data[i]["anilist"]["title"]["native"]).to_simple()] = [
                    data[i]["similarity"],
                    f"第{n}集",
                    f"约{int(from_m)}min{int(from_s)}s至{int(to_m)}min{int(to_s)}s处",
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

        return msg0


ani = Service("以图搜番").document("通过一张图片搜索你需要的番！据说里*也可以")


anime_search = ani.on_command("以图搜番", "发送一张图以搜索可能的番剧")


@anime_search.got("anime_pic", "图呢？", [Cooldown(5, prompt=_anime_flmt_notice)])
async def _deal_sear(bot: Bot, event: MessageEvent):
    user_id = event.get_user_id()
    img = extract_image_urls(event.message)
    if not img:
        await anime_search.finish("请发送图片而不是其它东西！！")

    await bot.send(event, "别急，在找了")
    a = await Anime(img[0]).do_search()
    result = f"> {MessageSegment.at(user_id)}\n" + a
    await anime_search.finish(Message(result))
