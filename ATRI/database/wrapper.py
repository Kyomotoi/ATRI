from typing import Type

from tortoise.models import Model


class DatabaseWrapper:
    def __init__(self, model: Type[Model]):
        self.model = model

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def add_sub(self, *args, **kwargs):
        await self.model.create(*args, **kwargs)

    async def update_sub(self, update_map: dict, **kwargs):
        await self.model.filter(**kwargs).update(**update_map)

    async def del_sub(self, query_map: dict):
        await self.model.filter(**query_map).delete()

    async def get_sub_list(self, query_map: dict) -> list:
        return await self.model.filter(**query_map)

    async def get_all_subs(self) -> list:
        return await self.model.all()
