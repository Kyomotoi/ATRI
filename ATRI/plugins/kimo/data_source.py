import json
from pathlib import Path
from jieba import posseg
from random import choice, shuffle

from ATRI.service import Service
from ATRI.rule import to_bot, is_in_service
from ATRI.log import logger as log
from ATRI.utils import request
from ATRI.exceptions import ReadFileError, WriteFileError


CHAT_PATH = Path(".") / "data" / "database" / "kimo"
CHAT_PATH.mkdir(parents=True, exist_ok=True)
KIMO_URL = "https://cdn.jsdelivr.net/gh/Kyomotoi/AnimeThesaurus/data.json"


class Kimo(Service):
    def __init__(self):
        Service.__init__(
            self, "kimo", "好像有点涩？", rule=to_bot() & is_in_service("kimo"), priority=5
        )

    @staticmethod
    async def _request(url: str) -> dict:
        res = await request.get(url)
        data = res.json()
        return data

    @classmethod
    async def _generate_data(cls) -> None:
        file_name = "kimo.json"
        path = CHAT_PATH / file_name
        if not path.is_file():
            log.warning("未检测到词库，生成中")
            data = await cls._request(KIMO_URL)
            try:
                with open(path, "w", encoding="utf-8") as w:
                    w.write(json.dumps(data, indent=4))
                log.info("生成完成")
            except WriteFileError:
                raise WriteFileError("Writing kimo words failed!")

    @classmethod
    async def _load_data(cls) -> dict:
        file_name = "kimo.json"
        path = CHAT_PATH / file_name
        if not path.is_file():
            await cls._generate_data()

        with open(path, "r", encoding="utf-8") as r:
            data = json.loads(r.read())
        return data

    @classmethod
    async def update_data(cls) -> None:
        log.info("更新闲聊词库ing...")
        file_name = "kimo.json"
        path = CHAT_PATH / file_name
        if not path.is_file():
            await cls._generate_data()

        updata_data = await cls._request(KIMO_URL)
        data = json.loads(path.read_bytes())
        for i in updata_data:
            if i not in data:
                data[i] = updata_data[i]

        with open(path, "w", encoding="utf-8") as w:
            w.write(json.dumps(data, indent=4))
        log.info("kimo词库更新完成")

    @staticmethod
    def name_is(user_id: str, new_name: str):
        file_name = "users.json"
        path = CHAT_PATH / file_name
        if not path.is_file():
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps({}))
            data = {}

        data = json.loads(path.read_bytes())
        data[user_id] = new_name
        try:
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps(data, indent=4))
        except ReadFileError:
            raise ReadFileError("Update user name failed!")

    @staticmethod
    def load_name(user_id: str) -> str:
        file_name = "users.json"
        path = CHAT_PATH / file_name
        if not path.is_file():
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps({}))
            return "你"

        data = json.loads(path.read_bytes())
        try:
            result = data[user_id]
        except BaseException:
            result = "你"
        return result

    @classmethod
    async def deal(cls, msg: str, user_id: str) -> str:
        keywords = posseg.lcut(msg)
        shuffle(keywords)

        data = await cls._load_data()

        repo = str()
        for i in keywords:
            a = i.word
            b = list(a)
            try:
                if b[0] == b[1]:
                    a = b[0]
            except BaseException:
                pass
            if a in data:
                repo = data.get(a, str())

        if not repo:
            temp_data = list(data)
            shuffle(temp_data)
            for i in temp_data:
                if i in msg:
                    repo = data.get(i, str())

        a = choice(repo) if type(repo) is list else repo
        user_name = cls.load_name(user_id)
        repo = a.replace("你", user_name)
        return repo
