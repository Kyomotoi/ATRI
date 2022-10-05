from ATRI.database import RssMikananiSubcription


class DB:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def add_sub(self, _id: str, group_id: int):
        await RssMikananiSubcription.create(_id=_id, group_id=group_id)

    async def update_sub(self, _id: str, group_id: int, update_map: dict):
        await RssMikananiSubcription.filter(_id=_id, group_id=group_id).update(
            **update_map
        )

    async def del_sub(self, query_map: dict):
        await RssMikananiSubcription.filter(**query_map).delete()

    async def get_sub_list(self, query_map: dict) -> list:
        return await RssMikananiSubcription.filter(**query_map)

    async def get_all_subs(self) -> list:
        return await RssMikananiSubcription.all()
