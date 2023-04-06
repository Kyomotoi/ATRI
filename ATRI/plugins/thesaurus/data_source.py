from datetime import datetime, timedelta, timezone as tz

from ATRI.message import MessageBuilder
from ATRI.exceptions import ThesaurusError
from ATRI.database import DatabaseWrapper, ThesaurusStoragor, ThesaurusAuditList


DBForTS = DatabaseWrapper(ThesaurusStoragor)
DBForTAL = DatabaseWrapper(ThesaurusAuditList)


class ThesaurusManager:
    async def __add_item(self, _id: str, group_id: int, is_main: bool = False):
        if is_main:
            try:
                await DBForTS.add_sub(_id=_id, group_id=group_id)
            except Exception:
                raise ThesaurusError(f"添加词库(ts)数据失败 目标词id: {_id}")
        else:
            try:
                await DBForTAL.add_sub(_id=_id, group_id=group_id)
            except Exception:
                raise ThesaurusError(f"添加词库(tal)数据失败 目标词id: {_id}")

    async def update_item(
        self, _id: str, group_id: int, update_map: dict, is_main: bool = False
    ):
        if is_main:
            try:
                await DBForTS.update_sub(
                    update_map=update_map, _id=_id, group_id=group_id
                )
            except Exception:
                raise ThesaurusError(f"更新词库(ts)数据失败 目标词id: {_id}")
        else:
            try:
                await DBForTAL.update_sub(
                    update_map=update_map, _id=_id, group_id=group_id
                )
            except Exception:
                raise ThesaurusError(f"更新词库(tal)数据失败 目标词id: {_id}")

    async def __del_item(self, _id: str, group_id: int, is_main: bool = False):
        if is_main:
            try:
                await DBForTS.del_sub({"_id": _id, "group_id": group_id})
            except Exception:
                raise ThesaurusError(f"删除词库(ts)数据失败 目标词id: {_id}")
        else:
            try:
                await DBForTAL.del_sub({"_id": _id, "group_id": group_id})
            except Exception:
                raise ThesaurusError(f"删除词库(tal)数据失败 目标词id: {_id}")

    async def get_item_list(self, query_map: dict, is_main: bool = False) -> list:
        if is_main:
            try:
                return await DBForTS.get_sub_list(query_map)
            except Exception:
                raise ThesaurusError("获取词库(ts)列表数据失败")
        else:
            try:
                return await DBForTAL.get_sub_list(query_map)
            except Exception:
                raise ThesaurusError("获取词库(tal)列表数据失败")

    async def get_all_items(self, is_main: bool = False) -> list:
        if is_main:
            try:
                return await DBForTS.get_all_subs()
            except Exception:
                raise ThesaurusError("获取全部词库(ts)列表数据失败")
        else:
            try:
                return await DBForTAL.get_all_subs()
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
            await self.del_item(_id, group_id, is_main)
            item_info = query_result[0]
            return (
                MessageBuilder(f"{str() if is_main else '(需审核/投票)'}该词条已存在!!")
                .text(f"ID: {item_info._id}")
                .text("因此, 此新增词条将被删除")
                .done()
            )

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
            "update_time": datetime.now(tz(timedelta(hours=8))),
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
                "update_time": datetime.now(tz(timedelta(hours=8))),
            },
        )


class ThesaurusListener:
    async def get_item_by_id(self, _id: str) -> ThesaurusStoragor:
        try:
            data = await DBForTS.get_sub_list({"_id": _id})
        except Exception:
            raise ThesaurusError(f"获取词库(ts)数据失败 词条ID: {_id}")

        return data[0]

    async def get_item_list(self, group_id: int):
        try:
            return await DBForTS.get_sub_list({"group_id": group_id})
        except Exception:
            raise ThesaurusError(f"获取词库(ts)数据失败 目标群号: {group_id}")
