import re

from pathlib import Path
from random import choice, randint
from nonebot.adapters.onebot.v11 import unescape

from ATRI.log import log
from ATRI.exceptions import RequestError
from ATRI.utils import request
from ATRI.utils import request, Translate


FUNNY_DIR = Path(".") / "data" / "plugins" / "funny"
FUNNY_DIR.mkdir(parents=True, exist_ok=True)


class Funny:
    @staticmethod
    async def idk_laugh(name: str) -> str:
        laugh_list = list()

        file_name = "laugh.txt"
        path = FUNNY_DIR / file_name
        if not path.is_file():
            log.warning("未发现笑话相关数据，正在下载并保存...")
            url = "https://jsd.imki.moe/gh/Kyomotoi/CDN@master/project/ATRI/laugh.txt"
            res = await request.get(url)
            context = res.text
            with open(path, "w", encoding="utf-8") as w:
                w.write(context)
            log.warning("完成")

        with open(path, "r", encoding="utf-8") as r:
            for line in r:
                laugh_list.append(line.strip("\n"))

        rd: str = choice(laugh_list)
        result = rd.replace("%name", name)
        return result

    @staticmethod
    def me_re_you(msg: str) -> tuple:
        if "我" in msg and "[CQ" not in msg:
            return msg.replace("我", "你"), True
        else:
            return msg, False

    @staticmethod
    def fake_msg(text: str) -> list:
        arg = text.split(" ")
        node = list()

        for i in arg:
            args = i.split("-")
            qq = args[0]
            name = unescape(args[1])
            repo = unescape(args[2])
            dic = {"type": "node", "data": {"name": name, "uin": qq, "content": repo}}
            node.append(dic)
        return node
