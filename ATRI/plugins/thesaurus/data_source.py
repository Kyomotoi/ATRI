import pytz
from datetime import datetime

from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import GROUP_OWNER, GROUP_ADMIN

from ATRI.service import Service
from ATRI.rule import is_in_service
from ATRI.exceptions import ThesaurusError

from .db import DBForTS, DBForTAL
from .db import ThesaurusStoragor


class ThesaurusManager(Service):
    def __init__(self):
        Service.__init__(
            self,
            "词库管理",
            "支持模糊匹配、全匹配、正则的自定义回复～\n支持分群、全局管理，支持群内投票添加",
            rule=is_in_service("词库管理"),
            permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN,
            main_cmd="/ts",
        )

    async def __add_item(self, _id: str, group_id: int, is_main: bool = False):
        if is_main:
            try:
                async with DBForTS() as db:
                    await db.add_item(_id, group_id)
            except Exception:
                raise ThesaurusError(f"添加词库(ts)数据失败 目标词id: {_id}")
        else:
            try:
                async with DBForTAL() as db:
                    await db.add_item(_id, group_id)
            except Exception:
                raise ThesaurusError(f"添加词库(tal)数据失败 目标词id: {_id}")

    async def update_item(
        self, _id: str, group_id: int, update_map: dict, is_main: bool = False
    ):
        if is_main:
            try:
                async with DBForTS() as db:
                    await db.update_item(_id, group_id, update_map)
            except Exception:
                raise ThesaurusError(f"更新词库(ts)数据失败 目标词id: {_id}")
        else:
            try:
                async with DBForTAL() as db:
                    await db.update_item(_id, group_id, update_map)
            except Exception:
                raise ThesaurusError(f"更新词库(tal)数据失败 目标词id: {_id}")

    async def __del_item(self, _id: str, group_id: int, is_main: bool = False):
        if is_main:
            try:
                async with DBForTS() as db:
                    await db.del_item({"_id": _id, "group_id": group_id})
            except Exception:
                raise ThesaurusError(f"删除词库(ts)数据失败 目标词id: {_id}")
        else:
            try:
                async with DBForTAL() as db:
                    await db.del_item({"_id": _id, "group_id": group_id})
            except Exception:
                raise ThesaurusError(f"删除词库(tal)数据失败 目标词id: {_id}")

    async def get_item_list(self, query_map: dict, is_main: bool = False) -> list:
        if is_main:
            try:
                async with DBForTS() as db:
                    return await db.get_item_list(query_map)
            except Exception:
                raise ThesaurusError("获取词库(ts)列表数据失败")
        else:
            try:
                async with DBForTAL() as db:
                    return await db.get_item_list(query_map)
            except Exception:
                raise ThesaurusError("获取词库(tal)列表数据失败")

    async def get_all_items(self, is_main: bool = False) -> list:
        if is_main:
            try:
                async with DBForTS() as db:
                    return await db.get_all_items()
            except Exception:
                raise ThesaurusError("获取全部词库(ts)列表数据失败")
        else:
            try:
                async with DBForTAL() as db:
                    return await db.get_all_items()
            except Exception:
                raise ThesaurusError("获取全部词库(tal)列表数据失败")

    async def add_item(
        self,
        _id: str,
        is_main: bool,
        q: str,
        a: list,
        need_at: int,
        t: str,
        group_id: int,
        operator: str,
        operator_id: int,
        is_vote: int,
        vote_list: list,
    ) -> str:
        query_result = await self.get_item_list(
            {"matcher": q, "group_id": group_id}, is_main
        )
        if query_result:
            item_info = query_result[0]
            return f"""{"(需审核/投票)" if not is_main else str()}该词条已存在！！ ID: {item_info._id}"""

        if t == "全匹配":
            m_type = 0
        elif t == "模糊匹配":
            m_type = 1
        else:
            m_type = 2

        item_meta = {
            "matcher": q,
            "result": a,
            "need_at": need_at,
            "m_type": m_type,
            "group_id": group_id,
            "operator": operator,
            "operator_id": operator_id,
            "update_time": datetime.now(pytz.timezone("Asia/Shanghai")),
            "is_vote": is_vote,
            "vote_list": vote_list,
        }

        await self.__add_item(_id, group_id, is_main)
        await self.update_item(
            _id,
            group_id,
            item_meta,
            is_main,
        )
        return f"""{"(需审核/投票)" if not is_main else str()}成功加上新词条 ID: {_id}"""

    async def del_item(self, _id: str, group_id: int, is_main: bool):
        query_result = await self.get_item_list(
            {"_id": _id, "group_id": group_id}, is_main
        )
        if not query_result:
            return f"目标id: {_id} 没有记录呢..."

        await self.__del_item(_id, group_id, is_main)
        return f"成功删除目标id: {_id} 问答信息"

    async def vote(self, _id: str, group_id: int, voter: int):
        raw_item_info = await self.get_item_list({"_id": _id, "group_id": group_id})
        item_info = raw_item_info[0]
        vote_list: list = item_info.vote_list
        vote_list.append(voter)

        await self.update_item(
            _id,
            group_id,
            {
                "vote_list": vote_list,
                "update_time": datetime.now(pytz.timezone("Asia/Shanghai")),
            },
        )


class ThesaurusListener(Service):
    def __init__(self):
        Service.__init__(self, "词库监听", "词库监听器", rule=is_in_service("词库监听"))

    async def get_item_by_id(self, _id: str) -> ThesaurusStoragor:
        try:
            async with DBForTS() as db:
                data = await db.get_item_list({"_id": _id})
        except Exception:
            raise ThesaurusError(f"获取词库(ts)数据失败 词条ID: {_id}")

        return data[0]

    async def get_item_list(self, group_id: int):
        try:
            async with DBForTS() as db:
                return await db.get_item_list({"group_id": group_id})
        except Exception:
            raise ThesaurusError(f"获取词库(ts)数据失败 目标群号: {group_id}")
