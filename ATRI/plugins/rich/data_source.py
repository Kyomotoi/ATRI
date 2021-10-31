import re

from ATRI.service import Service
from ATRI.utils import request
from ATRI.rule import is_in_service
from ATRI.exceptions import RequestError


URL = "https://api.kyomotoi.moe/api/bilibili/v3/video_info?aid="

table = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF"
tr = dict()
for i in range(58):
    tr[table[i]] = i
s = [11, 10, 3, 8, 4, 6]
xor = 177451812
add = 8728348608

__doc__ = """啥b腾讯小程序给👴爪巴
目前只整了b站的
"""


class Rich(Service):
    def __init__(self):
        Service.__init__(self, "小程序处理", __doc__, rule=is_in_service("小程序处理"))

    @staticmethod
    def _bv_dec(x) -> str:
        r = 0
        for i in range(6):
            r += tr[x[s[i]]] * 58 ** i
        result = "av" + str((r - add) ^ xor)
        return result

    @staticmethod
    def _bv_enc(x) -> str:
        x = (x ^ xor) + add
        r = list("BV1  4 1 7  ")
        for i in range(6):
            r[s[i]] = table[x // 58 ** i % 58]
        return "".join(r)

    @classmethod
    async def fk_bili(cls, text: str) -> tuple:
        msg = text.replace("\\", "")
        bv = False
        if "https://b23" in msg:
            pattern = r"https://b23\.tv/[a-zA-Z0-9]+"
            burl = re.findall(pattern, msg)
            u = burl[0]

            try:
                res = await request.get(u)
            except:
                return "Request failed!", False

            bv_pattern = r"video/BV[a-zA-Z0-9]+"
            try:
                tu = str(res.url)
                t_bv = re.findall(bv_pattern, tu)
                bv = t_bv[0].replace("video/", "")
            except:
                return "Deal bv code failed!", False
            av = cls._bv_dec(bv).replace("av", "")

        else:
            pattern = r"[bB][vV][a-zA-Z0-9]+"
            try:
                bv = re.findall(pattern, msg)[0]
            except:
                return "Deal bv code failed!", False
            av = cls._bv_dec(bv).replace("av", "")

        url = URL + av
        try:
            res = await request.get(url)
        except RequestError:
            return "Request failed!", False
        res_data = res.json()
        data = res_data["data"]

        result = (
            f"{data['bvid']} INFO:\n"
            f"Title: {data['title']}\n"
            f"Link: {data['short_link']}"
        )
        return result, True
