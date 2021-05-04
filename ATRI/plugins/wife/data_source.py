import os
import json
from pathlib import Path


WIFE_DIR = Path(".") / "ATRI" / "data" / "database" / "wife"
MERRY_LIST_PATH = WIFE_DIR / "merry_list.json"
os.makedirs(WIFE_DIR, exist_ok=True)


class Tsuma:
    @staticmethod
    def _load_tsuma() -> dict:
        try:
            return json.loads(MERRY_LIST_PATH.read_bytes())
        except FileNotFoundError:
            with open(MERRY_LIST_PATH, "w") as r:
                r.write(json.dumps({}, indent=4))
            return dict()

    @staticmethod
    def _store_tsuma(data: dict) -> None:
        with open(MERRY_LIST_PATH, "w") as r:
            r.write(json.dumps(data, indent=4))

    @classmethod
    def check_tsuma(cls, user: str):
        data = cls._load_tsuma()
        if user in data:
            msg = "阿，你已经有老婆惹！" f"ta是：{data[user]['lassie']['nickname']}"
            return msg, True
        else:
            return "悲——你还没老婆...", False

    @classmethod
    def inquire_tsuma(cls, user: str) -> str:
        data = cls._load_tsuma()
        if user in data:
            return f"你的老婆是：{data[user]['lassie']['nickname']} 哦~❤"
        else:
            return "悲——你还没老婆..."

    @classmethod
    def got_tsuma(cls, user: str, d: dict) -> str:
        check_repo, if_h = cls.check_tsuma(user)  # 防止出现多人同时操作导致 NTR 事件
        if if_h:
            return check_repo
        else:
            data = cls._load_tsuma()
            data[user] = {
                "nickname": d["nickname"],
                "gender": d["gender"],
                "lassie": {
                    "nickname": d["lassie"]["nickname"],
                    "qq": d["lassie"]["qq"],
                    "gender": d["lassie"]["gender"],
                },
            }
            cls._store_tsuma(data)

            data[d["lassie"]["qq"]] = {
                "nickname": d["lassie"]["nickname"],
                "gender": d["lassie"]["gender"],
                "lassie": {
                    "nickname": d["nickname"],
                    "qq": user,
                    "gender": d["gender"],
                },
            }
            cls._store_tsuma(data)

            msg = (
                f"> {d['lassie']['nickname']}({d['lassie']['qq']})\n"
                f"恭喜成为 {d['nickname']} 的老婆~⭐"
            )
            return msg

    @classmethod
    def divorce(cls, user: str) -> str:
        data = cls._load_tsuma()
        if not user in data:
            return "悲——你还没老婆。。"

        msg = f"悲——，({data[user]['nickname']})抛弃了({data[user]['lassie']['nickname']})"
        del data[user]
        cls._store_tsuma(data)
        return msg
