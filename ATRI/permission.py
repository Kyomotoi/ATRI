import json

from nonebot.adapters import Bot, Event
from nonebot.permission import Permission as _Permission
from nonebot.adapters.onebot.v11 import GROUP_OWNER, GROUP_ADMIN as _GROUP_ADMIN
from nonebot.adapters.onebot.v11 import GroupMessageEvent

from ATRI import conf
from ATRI.configs.config import CONFIG_PATH


MASTER_FILE_PATH = CONFIG_PATH / "master.json"
if not MASTER_FILE_PATH.is_file():
    with open(MASTER_FILE_PATH, "w") as w:
        w.write(json.dumps(list()))

MASTER_LIST = set()


def init_permission():
    global MASTER_LIST
    data = json.loads(MASTER_FILE_PATH.read_bytes())
    MASTER_LIST = set.union(set(data), conf.BotConfig.superusers)


def is_master(bot: Bot, event: Event) -> bool:
    init_permission()
    try:
        user_id = event.get_user_id()
    except Exception:
        return False

    return True if user_id in MASTER_LIST else False


class Permission(_Permission):
    name = str()

    def set_name(self, name: str) -> "Permission":
        """为当前权限设置名称

        Args:
            name (str): 权限的名称
        """
        self.name = name
        return self


class MasterList:
    """检查当前事件是否属于主人"""

    __slots__ = ()

    async def __call__(self, bot: Bot, event: Event) -> bool:
        return is_master(bot, event)


class Admin:
    """检查当前事件是否属于管理员"""

    __slots__ = ()

    GROUP_ADMIN = ["admin", "owner"]

    async def __call__(self, bot: Bot, event: Event) -> bool:
        if isinstance(event, GroupMessageEvent):
            return True if event.sender.role in ["admin", "owner"] else False
        else:
            return is_master(bot, event)


init_permission()
MASTER = Permission(MasterList()).set_name("Master")
ADMIN = Permission(Admin()).set_name("Admin")