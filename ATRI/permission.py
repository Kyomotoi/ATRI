import json

from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER, Permission
from nonebot.adapters.onebot.v11 import GROUP_OWNER, GROUP_ADMIN as _GROUP_ADMIN

from ATRI.configs.config import CONFIG_PATH


MASTER_FILE_PATH = CONFIG_PATH / "master.json"
if not MASTER_FILE_PATH.is_file():
    with open(MASTER_FILE_PATH, "w") as w:
        w.write(json.dumps(list()))


class MasterList:
    """检查当前事件是否属于主人"""

    __slots__ = ()

    async def __call__(self, bot: Bot, event: Event) -> bool:
        try:
            user_id = event.get_user_id()
        except Exception:
            return False

        data = json.loads(MASTER_FILE_PATH.read_bytes())
        return True if user_id in data else False


MASTER = SUPERUSER | Permission(MasterList())
GROUP_ADMIN = GROUP_OWNER | _GROUP_ADMIN
ADMIN = MASTER | GROUP_ADMIN
