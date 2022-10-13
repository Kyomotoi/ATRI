from datetime import datetime

from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import GROUP_OWNER, GROUP_ADMIN

from ATRI import driver
from ATRI.service import Service, ServiceTools
from ATRI.rule import is_in_service
from ATRI.log import log
from ATRI.utils import request
from ATRI.utils.apscheduler import scheduler
from ATRI.message import MessageBuilder
from ATRI.exceptions import TwitterDynamicError

from .db import DB
from .api import API


_DYNAMIC_OUTPUT_FORMAT = (
    MessageBuilder("{t_nickname} 的推更新了！")
    .text("{t_dy_content}")
    .done()
)


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

    async def __add_sub(self, tid: int, group_id: int):
        try:
            async with DB() as db:
                await db.add_sub(tid, group_id)
        except Exception:
            raise TwitterDynamicError("添加订阅失败")

    async def update_sub(self, tid: int, group_id: int, update_map: dict):
        try:
            async with DB() as db:
                await db.update_sub(tid, group_id, update_map)
        except Exception:
            raise TwitterDynamicError("更新订阅失败")

    async def __del_sub(self, tid: int, group_id: int):
        try:
            async with DB() as db:
                await db.del_sub({"tid": tid, "group_id": group_id})
        except Exception:
            raise TwitterDynamicError("删除订阅失败")

    async def get_sub_list(self, tid: int = int(), group_id: int = int()) -> list:
        if not tid:
            query_map = {"group_id": group_id}
        else:
            query_map = {"tid": tid, "group_id": group_id}

        try:
            async with DB() as db:
                return await db.get_sub_list(query_map)
        except Exception:
            raise TwitterDynamicError("获取订阅列表失败")

    async def get_all_subs(self) -> list:
        try:
            async with DB() as db:
                return await db.get_all_subs()
        except Exception:
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

        return _DYNAMIC_OUTPUT_FORMAT.format(
            t_nickname=data["name"],
            t_dy_content=str(content)
            .replace("https://", str())
            .replace("http://", str()),
        )

    async def add_sub(self, name: str, group_id: int) -> str:
        t_name, t_screen_name = await self.get_twitter_username(name)
        if not t_name or not t_screen_name:
            return f"无法获取名为 {name} 的推主的信息...操作失败了"

        res = await self.get_twitter_user_info(name)
        tid = res["id"]

        query_result = await self.get_sub_list(tid, group_id)
        if query_result:
            return f"该推主 {t_name}@{t_screen_name}\n已在本群订阅列表中啦！"

        await self.__add_sub(tid, group_id)
        await self.update_sub(
            tid,
            group_id,
            {
                "name": t_name,
                "screen_name": t_screen_name,
                "last_update": datetime.utcnow(),
            },
        )
        return f"成功订阅名为 {t_name}@{t_screen_name} 推主的动态～！"

    async def del_sub(self, tid: int, group_id: int) -> str:
        query_result = await self.get_sub_list(tid, group_id)
        if not query_result:
            return f"取消订阅失败...该tid: {tid} 不在本群订阅列表中"

        await self.__del_sub(tid, group_id)
        return f"成功取消tid为 {tid} 推主的订阅～"


# TODO
# class TwitterHelper(Service):
#     def __init__(self):
#         Service.__init__(self, "推特助手", "推特小助手", rule=is_in_service("推特助手"))


async def _regot_in_need():
    api = API()
    await api.get_token()
    # await api.get_cookie()


async def _check_status():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    try:
        await request.get("https://twitter.com/", headers=headers)
        log.success("已成功连接: Twitter")
        await _regot_in_need()
        scheduler.add_job(_regot_in_need, "interval", name="刷新推特凭据", minutes=30, misfire_grace_time=10)  # type: ignore
    except Exception:
        ServiceTools.service_controller("推特动态订阅", False)
        log.warning("无法连接至 Twitter，这将导致相关插件无法工作. 已自动禁用.")


driver().on_startup(_check_status)
