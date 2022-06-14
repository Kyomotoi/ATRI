from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11 import GROUP_OWNER, GROUP_ADMIN

from ATRI.service import Service
from ATRI.rule import is_in_service
from ATRI.exceptions import TwitterDynamicError

from .db import DB
from .api import API


_DYNAMIC_OUTPUT_FORMAT = """
{t_nickname} 的推更新了！
（限制 {limit_content} 字）
{t_dy_content}
{t_dy_media}
链接: {t_dy_link}
""".strip()


class TwitterDynamicSubscriptor(Service):
    def __init__(self):
        Service.__init__(
            self,
            "推特动态订阅",
            "推特动态订阅助手～",
            rule=is_in_service("推特动态订阅"),
            permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN,
            main_cmd="/td",
        )

    async def add_sub(self, tid: int, group_id: int):
        try:
            async with DB() as db:
                await db.add_sub(tid, group_id)
        except TwitterDynamicError:
            raise TwitterDynamicError("添加订阅失败")

    async def update_sub(self, tid: int, update_map: dict):
        try:
            async with DB() as db:
                await db.update_sub(tid, update_map)
        except TwitterDynamicError:
            raise TwitterDynamicError("更新订阅失败")

    async def del_sub(self, screen_name: str, group_id: int):
        try:
            async with DB() as db:
                await db.del_sub({"screen_name": screen_name, "group_id": group_id})
        except TwitterDynamicError:
            raise TwitterDynamicError("删除订阅失败")

    async def get_sub_list(self, tid: int = int(), group_id: int = int()) -> list:
        if not tid:
            query_map = {"group_id": group_id}
        else:
            query_map = {"tid": tid, "group_id": group_id}

        try:
            async with DB() as db:
                return await db.get_sub_list(query_map)
        except TwitterDynamicError:
            raise TwitterDynamicError("获取订阅列表失败")

    async def get_all_subs(self) -> list:
        try:
            async with DB() as db:
                return await db.get_all_subs()
        except TwitterDynamicError:
            raise TwitterDynamicError("获取全部订阅列表失败")

    async def get_twitter_user_info(self, name: str) -> dict:
        api = API()
        resp = await api.search_user(name)
        return resp

    async def get_twitter_username(self, name: str) -> tuple:
        data = await self.get_twitter_user_info(name)
        _name = data.get("name", None)
        screen_name = data.get("screen_name", None)
        return _name, screen_name

    async def gen_output(self, data: dict, limit_content: int = 100) -> str:
        """生成动态信息

        Args:
            data (dict): dict形式的动态数据.
            limit_content (int, optional): 内容字数限制. 默认 100.

        Returns:
            str: 动态信息
        """
        return _DYNAMIC_OUTPUT_FORMAT.format(
            t_nickname=data["name"],
            limit_content=limit_content,
            t_dy_content=str(data["content"][:limit_content])
            .replace("https://", str())
            .replace("http://", str()),
            t_dy_media=MessageSegment.image(data["pic"]) if data.get("pic") else str(),
            t_dy_link="twitter.com/nihui/status/" + data["s_id"],
        )


# TODO
# class TwitterHelper(Service):
#     def __init__(self):
#         Service.__init__(self, "推特助手", "推特小助手", rule=is_in_service("推特助手"))
