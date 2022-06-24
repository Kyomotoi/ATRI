import json
from datetime import datetime
from operator import itemgetter

from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import GROUP_OWNER, GROUP_ADMIN

from ATRI.service import Service
from ATRI.rule import is_in_service
from ATRI.utils import timestamp2datetime
from ATRI.exceptions import BilibiliDynamicError

from .db import DB
from .api import API


_OUTPUT_FORMAT = """
{up_nickname} 的{up_dy_type}更新了！
（限制 {limit_content} 字）
{up_dy_content}
链接: {up_dy_link}
""".strip()


class BilibiliDynamicSubscriptor(Service):
    def __init__(self):
        Service.__init__(
            self,
            "b站动态订阅",
            "b站动态订阅助手～",
            rule=is_in_service("b站动态订阅"),
            permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN,
            main_cmd="/bd",
        )

    async def __add_sub(self, uid: int, group_id: int):
        try:
            async with DB() as db:
                await db.add_sub(uid, group_id)
        except Exception:
            raise BilibiliDynamicError("添加订阅失败")

    async def update_sub(self, uid: int, group_id: int, update_map: dict):
        try:
            async with DB() as db:
                await db.update_sub(uid, group_id, update_map)
        except Exception:
            raise BilibiliDynamicError("更新订阅失败")

    async def __del_sub(self, uid: int, group_id: int):
        try:
            async with DB() as db:
                await db.del_sub({"uid": uid, "group_id": group_id})
        except Exception:
            raise BilibiliDynamicError("删除订阅失败")

    async def get_sub_list(self, uid: int = int(), group_id: int = int()) -> list:
        if not uid:
            query_map = {"group_id": group_id}
        else:
            query_map = {"uid": uid, "group_id": group_id}

        try:
            async with DB() as db:
                return await db.get_sub_list(query_map)
        except Exception:
            raise BilibiliDynamicError("获取订阅列表失败")

    async def get_all_subs(self) -> list:
        try:
            async with DB() as db:
                return await db.get_all_subs()
        except Exception:
            raise BilibiliDynamicError("获取全部订阅列表失败")

    async def __get_up_nickname(self, uid: int) -> str:
        api = API(uid)
        resp = await api.get_user_info()
        data = resp.get("data", dict())
        return data.get("name", "unknown")

    async def get_up_recent_dynamic(self, uid: int) -> dict:
        api = API(uid)
        resp = await api.get_user_dynamics()
        data = resp.get("data", dict())
        if not data:
            return dict()

        if "cards" in data:
            for card in data["cards"]:
                card["card"] = json.loads(card["card"])
                card["extend_json"] = json.loads(card["extend_json"])
        return data

    def extract_dyanmic(self, data: list) -> list:
        result = list()
        for i in data:
            pattern = {}
            desc = i["desc"]
            card = i["card"]
            type = desc["type"]

            # common 部分
            pattern["type"] = desc["type"]
            pattern["uid"] = desc["uid"]
            pattern["view"] = desc["view"]
            pattern["repost"] = desc["repost"]
            pattern["like"] = desc["like"]
            pattern["dynamic_id"] = desc["dynamic_id"]
            pattern["timestamp"] = desc["timestamp"]
            pattern["time"] = timestamp2datetime(desc["timestamp"])
            pattern["type_zh"] = str()

            # alternative 部分
            pattern["content"] = str()
            pattern["pic"] = str()

            # 根据type区分 提取content
            if type == 1:  # 转发动态
                pattern["type_zh"] = "转发动态"
                pattern["content"] = card["item"]["content"]
                pattern["pic"] = card["user"]["face"]

            elif type == 2:  # 普通动态（带多张图片）
                pattern["type_zh"] = "普通动态（附图）"
                pattern["content"] = card["item"]["description"]
                if card["item"]["pictures_count"] > 0:
                    if isinstance(card["item"]["pictures"][0], str):
                        pattern["pic"] = card["item"]["pictures"][0]
                    else:
                        pattern["pic"] = card["item"]["pictures"][0]["img_src"]

            elif type == 4:  # 普通动态（纯文字）
                pattern["type_zh"] = "普通动态（纯文字）"
                pattern["content"] = card["item"]["content"]
                # 无图片

            elif type == 8:  # 视频动态
                pattern["type_zh"] = "视频动态"
                pattern["content"] = card["title"] + card["dynamic"]
                pattern["pic"] = card["pic"]

            elif type == 64:  # 文章
                pattern["type_zh"] = "文章"
                pattern["content"] = card["title"] + card["summary"]
                if len(card["image_urls"]) > 0:
                    pattern["pic"] = card["image_urls"][0]

            result.append(pattern)
        return sorted(result, key=itemgetter("timestamp"))

    def gen_output(self, data: dict, content_limit) -> str:
        """生成动态信息

        Args:
            data (dict): dict形式的动态数据.
            limit_content (int, optional): 内容字数限制.

        Returns:
            str: 动态信息
        """
        if not content_limit:
            content = data["content"]
        else:
            content = data["content"][:content_limit]

        return _OUTPUT_FORMAT.format(
            up_nickname=data["name"],
            up_dy_type=data["type_zh"],
            limit_content=content_limit,
            up_dy_content=str(content)
            .replace("https://", str())
            .replace("http://", str()),
            up_dy_link="https://t.bilibili.com/" + str(data["dynamic_id"]),
        )

    async def add_sub(self, uid: int, group_id: int) -> str:
        up_nickname = await self.__get_up_nickname(uid)
        if not up_nickname:
            return f"无法获取id为 {uid} 的up主信息...操作失败了"

        query_result = await self.get_sub_list(uid, group_id)
        if query_result:
            return f"该up主 {up_nickname} 已在本群订阅列表中啦！"

        await self.__add_sub(uid, group_id)
        await self.update_sub(
            uid,
            group_id,
            {"up_nickname": up_nickname, "last_update": datetime.utcnow()},
        )
        return f"成功订阅名为 {up_nickname} up主的动态～！"

    async def del_sub(self, uid: int, group_id: int) -> str:
        query_result = await self.get_sub_list(uid, group_id)
        if not query_result:
            return f"该uid: {uid} 未在本群订阅列表中啦！"

        await self.__del_sub(uid, group_id)
        return f"成功取消订阅uid为 {uid} up主的动态～！"
