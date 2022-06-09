import json
from random import choice
from pathlib import Path
from nonebot.adapters.onebot.v11 import MessageSegment

from ATRI.service import Service
from ATRI.rule import is_in_service


WIFE_DIR = Path(".") / "data" / "database" / "wife"
WIFE_DIR.mkdir(parents=True, exist_ok=True)


class Wife(Service):
    def __init__(self):
        Service.__init__(self, "老婆", "老婆...嘿嘿嘿...", rule=is_in_service("老婆"))

    def to_superuser(self, user_id: str):
        """
        全自动贴贴机，限制只有超级管理员才能贴贴
        """
        content = choice(
            [
                "mua！",
                "贴贴！",
                MessageSegment.image(
                    file="https://cdn.jsdelivr.net/gh/Kyomotoi/CDN@master/project/ATRI/wife0.jpg"
                ),
                MessageSegment.image(
                    file="https://cdn.jsdelivr.net/gh/Kyomotoi/CDN@master/project/ATRI/wife1.jpg"
                ),
                MessageSegment.image(
                    file="https://cdn.jsdelivr.net/gh/Kyomotoi/CDN@master/project/ATRI/wife2.jpg"
                ),
                MessageSegment.image(
                    file="https://cdn.jsdelivr.net/gh/Kyomotoi/CDN@master/project/ATRI/wife3.jpg"
                ),
            ]
        )
        result = MessageSegment.at(user_id) + content  # type: ignore
        return result

    @staticmethod
    def load_marry_list() -> dict:
        """
        读取结婚列表
        """
        file_name = "marry_list.json"
        path = WIFE_DIR / file_name
        if not path.is_file():
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps({}))

        data = json.loads(path.read_bytes())
        return data

    @staticmethod
    def save_marry_list(data: dict) -> None:
        """
        存储结婚列表
        """
        file_name = "marry_list.json"
        path = WIFE_DIR / file_name
        if not path.is_file():
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps({}))

        with open(path, "w", encoding="utf-8") as w:
            w.write(json.dumps(data, indent=4))
