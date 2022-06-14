from ATRI.database import TwitterSubscription


class DB:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def add_sub(self, tid: int, group_id: int):
        await TwitterSubscription.create(tid=tid, group_id=group_id)

    async def update_sub(self, tid: int, update_map: dict):
        await TwitterSubscription.filter(tid=tid).update(**update_map)

    async def del_sub(self, query_map: dict):
        await TwitterSubscription.filter(**query_map).delete()

    async def get_sub_list(self, query_map: dict) -> list:
        return await TwitterSubscription.filter(**query_map)

    async def get_all_subs(self) -> list:
        return await TwitterSubscription.all()
