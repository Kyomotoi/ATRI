from ATRI.database import ThesaurusStoragor, ThesaurusAuditList


class DBForTS:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def add_item(self, _id: str, group_id: int):
        await ThesaurusStoragor.create(_id=_id, group_id=group_id)

    async def update_item(self, _id: str, group_id: int, update_map: dict):
        await ThesaurusStoragor.filter(_id=_id, group_id=group_id).update(**update_map)

    async def del_item(self, query_map: dict):
        await ThesaurusStoragor.filter(**query_map).delete()

    async def get_item_list(self, query_map: dict) -> list:
        return await ThesaurusStoragor.filter(**query_map)

    async def get_all_items(self) -> list:
        return await ThesaurusStoragor.all()


class DBForTAL:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def add_item(self, _id: str, group_id: int):
        await ThesaurusAuditList.create(_id=_id, group_id=group_id)

    async def update_item(self, _id: str, group_id: int, update_map: dict):
        await ThesaurusAuditList.filter(_id=_id, group_id=group_id).update(**update_map)

    async def del_item(self, query_map: dict):
        await ThesaurusAuditList.filter(**query_map).delete()

    async def get_item_list(self, query_map: dict) -> list:
        return await ThesaurusAuditList.filter(**query_map)

    async def get_all_items(self) -> list:
        return await ThesaurusAuditList.all()
