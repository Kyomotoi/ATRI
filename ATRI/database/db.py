from pathlib import Path
from tortoise import Tortoise, run_async

from ATRI.log import logger as log


# 临时的实现，寻求更好的方式！欢迎pr


DB_DIR = Path(".") / "data" / "sql"
DB_DIR.mkdir(parents=True, exist_ok=True)


async def run():
    from ATRI.database import models

    await Tortoise.init(
        db_url=f"sqlite://{DB_DIR}/db.sqlite3",
        modules={"models": [locals()["models"]]},
    )
    await Tortoise.generate_schemas()


def init_database():
    log.info("正在初始化数据库...")
    run_async(run())
    log.success("数据库初始化完成")
