from pathlib import Path
from tortoise import Tortoise

from ATRI import driver
from .models import Subscription


DB_DIR = Path(".") / "data" / "database" / "bilibili_dynamic"
DB_DIR.mkdir(parents=True, exist_ok=True)


class DB:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def init(self):
        from . import models

        await Tortoise.init(
            db_url=f"sqlite://{DB_DIR}/db.sqlite3",
            modules={"models": [locals()["models"]]},
        )
        await Tortoise.generate_schemas()

    async def add_sub(self, uid: int, group_id: int):
        await Subscription.create(uid=uid, group_id=group_id)

    async def update_sub(self, uid: int, update_map: dict):
        await Subscription.filter(uid=uid).update(**update_map)

    async def del_sub(self, query_map: dict):
        await Subscription.filter(**query_map).delete()

    async def get_sub_list(self, query_map: dict) -> list:
        return await Subscription.filter(**query_map)

    async def get_all_subs(self) -> list:
        return await Subscription.all()


async def init():
    async with DB() as db:
        await db.init()


driver().on_startup(init)
