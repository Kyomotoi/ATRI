from tortoise import Tortoise

from ATRI.database import models
from nonebot import get_driver


# 关于数据库的操作类，只实现与数据库有关的CRUD
# 请不要把业务逻辑写进去
class DB:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def init(self):
        from ATRI.database import models

        await Tortoise.init(
            db_url="sqlite://ATRI/database/db.sqlite3",
            modules={"models": [locals()["models"]]},
        )
        # Generate the schema
        await Tortoise.generate_schemas()

    async def add_subscription(self, uid: int, groupid: int) -> bool:
        try:
            _ = await models.Subscription.create(uid=uid, groupid=groupid)
            return True
        except:
            return False

    async def get_all_subscriptions_by_gid(self, groupid: int) -> list:
        try:
            subs = await self.get_subscriptions(query_map={"groupid": groupid})
            return subs
        except:
            return []

    async def remove_subscription(self, query_map: dict) -> bool:
        try:
            ret = await models.Subscription.filter(**query_map).delete()
            return True
        except:
            return False

    async def get_subscriptions(self, query_map: dict) -> list:
        try:
            ret = await models.Subscription.filter(**query_map)
            return ret
        except:
            return []

    async def get_all_subscriptions(self) -> list:
        try:
            ret = await models.Subscription.all()
            return ret
        except:
            return []

    async def update_subscriptions_by_uid(self, uid: int, update_map: dict) -> bool:
        try:
            # why use ** ?
            # Reference: https://stackoverflow.com/questions/5710391/converting-python-dict-to-kwargs
            _ = await models.Subscription.filter(uid=uid).update(**update_map)
            return True
        except:
            return False


async def init():
    async with DB() as db:
        await db.init()


driver = get_driver()
driver.on_startup(init)
