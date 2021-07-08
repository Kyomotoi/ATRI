import re

from ATRI.service import Service
from ATRI.utils import request
from ATRI.rule import is_in_service
from ATRI.exceptions import RequestError


URL = f"https://api.kyomotoi.moe/api/bilibili/v2/?aid="

table = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF"
tr = dict()
for i in range(58):
    tr[table[i]] = i
s = [11, 10, 3, 8, 4, 6]
xor = 177451812
add = 8728348608


__doc__ = """
啥b腾讯小程序给👴爪巴
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
        """
        为何本函数这么多 try，因为此函数被用于监听所有信息
        如果真出现错误，就会一直刷屏
        """
        msg = text.replace("\\", "")
        bv = False

        if "qqdocurl" not in msg:
            if "av" in msg:
                av = re.findall(r"(av\d+)", msg)
                if not av:
                    return "Get value (av) failed!", False
                av = av[0].replace("av", "")
            else:
                bv = re.findall(r"([Bb][Vv]\w+)", msg)
                if not bv:
                    return "Get value (bv) failed!", False
                av = str(cls._bv_dec(bv[0])).replace("av", "")
        else:
            pattern = r"(?:(?:https?):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+"
            bv_url = re.findall(pattern, msg)
            if not bv_url:
                return "Get value (bv url) failed!", False
            bv_url = bv_url[3]

            try:
                res = await request.get(bv_url)
            except RequestError:
                return "Request failed!", False
            bv = re.findall(r"(BV\w+)", str(res.url))
            if not bv:
                return "Get value (bv) failed!", False
            av = cls._bv_dec(bv[0])

        if not bv:
            if "av" in msg:
                av = re.findall(r"(av\d+)", msg)
                if not av:
                    return "Get value (av) failed!", False
                av = av[0].replace("av", "")
            else:
                return "Not found av", False

        url = URL + av
        try:
            res = await request.get(url)
        except RequestError:
            return "Request failed!", False
        res_data = await res.json()
        data = res_data["data"]

        result = (
            f"{data['bvid']} INFO:\n"
            f"Title: {data['title']}\n"
            f"Link: {data['short_link']}"
        )
        return result, True
