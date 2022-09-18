import xmltodict

from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import GROUP_OWNER, GROUP_ADMIN

from ATRI.service import Service
from ATRI.rule import is_in_service
from ATRI.exceptions import RssError
from ATRI.utils import request, gen_random_str

from .db import DB


class RssHubSubscriptor(Service):
    def __init__(self):
        Service.__init__(
            self,
            "rss.rsshub",
            "Rss的Rsshub支持",
            rule=is_in_service("rss.rsshub"),
            permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN,
            main_cmd="/rss.rsshub",
        )

    async def __add_sub(self, _id: str, group_id: int):
        try:
            async with DB() as db:
                await db.add_sub(_id, group_id)
        except Exception:
            raise RssError("rss.rsshub: 添加订阅失败")

    async def update_sub(self, _id: str, group_id: int, update_map: dict):
        try:
            async with DB() as db:
                await db.update_sub(_id, group_id, update_map)
        except Exception:
            raise RssError("rss.rsshub: 更新订阅失败")

    async def __del_sub(self, _id: str, group_id: int):
        try:
            async with DB() as db:
                await db.del_sub({"_id": _id, "group_id": group_id})
        except Exception:
            raise RssError("rss.rsshub: 删除订阅失败")

    async def get_sub_list(self, query_map: dict) -> list:
        try:
            async with DB() as db:
                return await db.get_sub_list(query_map)
        except Exception:
            raise RssError("rss.rsshub: 获取订阅列表失败")

    async def get_all_subs(self) -> list:
        try:
            async with DB() as db:
                return await db.get_all_subs()
        except Exception:
            raise RssError("rss.rsshub: 获取所有订阅失败")

    async def add_sub(self, url: str, group_id: int) -> str:
        try:
            resp = await request.get(url)
        except Exception:
            raise RssError("rss.rsshub: 请求链接失败")

        if "RSSHub" not in resp.text:
            return "该链接不含RSSHub内容"

        xml_data = resp.read()
        data = xmltodict.parse(xml_data)
        check_url = data["rss"]["channel"]["link"]

        query_result = await self.get_sub_list(
            {"raw_link": check_url, "group_id": group_id}
        )
        if query_result:
            _id = query_result[0]._id
            return f"该链接已经订阅过啦! ID: {_id}"

        _id = gen_random_str(6)
        title = data["rss"]["channel"]["title"]
        disc = data["rss"]["channel"]["description"]

        await self.__add_sub(_id, group_id)
        await self.update_sub(
            _id,
            group_id,
            {
                "title": title,
                "rss_link": url,
                "discription": disc,
            },
        )
        return f"订阅成功! ID: {_id}"

    async def del_sub(self, _id: str, group_id: int) -> str:
        query_result = await self.get_sub_list({"_id": _id, "group_id": group_id})
        if not query_result:
            return "没有找到该订阅..."

        await self.__del_sub(_id, group_id)
        return f"成功取消ID为 {_id} 的订阅"

    async def get_rsshub_info(self, url: str) -> dict:
        try:
            resp = await request.get(url)
        except Exception:
            raise RssError("rss.rsshub: 请求链接失败")

        if "RSSHub" not in resp.text:
            return dict()

        xml_data = resp.read()
        data = xmltodict.parse(xml_data)
        return data["rss"]["channel"]
