import json

from nonebot.adapters import Bot, Event
from nonebot.permission import Permission as _Permission
from nonebot.adapters.onebot.v11 import GroupMessageEvent

from ATRI import conf
from ATRI.utils import FileDealer
from ATRI.configs.config import CONFIG_DATA_PATH


MASTER_FILE_PATH = CONFIG_DATA_PATH / "master.json"
MASTER_FILE = FileDealer(MASTER_FILE_PATH)
MASTER_LIST = set()


def create_master_file():
    if not MASTER_FILE_PATH.is_file():
        data = dict()
        for i in conf.BotConfig.superusers:
            data[i] = {"is_conf": True}

        with open(MASTER_FILE_PATH, "w") as w:
            w.write(json.dumps(data))


def init_permission():
    global MASTER_LIST
    create_master_file()
    data = MASTER_FILE.json()
    MASTER_LIST = set.union(set(data), conf.BotConfig.superusers)


def is_master(bot: Bot, event: Event) -> bool:
    init_permission()
    try:
        user_id = event.get_user_id()
    except Exception:
        return False

    return user_id in MASTER_LIST


class Permission(_Permission):
    name = str()

    def set_name(self, name: str) -> "Permission":
        """为当前权限设置名称

        Args:
            name (str): 权限的名称

        Returns:
            Permission: self
        """
        self.name = name
        return self


class Master:
    """检查当前事件是否属于主人"""

    __slots__ = ()

    async def __call__(self, bot: Bot, event: Event) -> bool:
        return is_master(bot, event)


class Admin:
    """
    检查当前事件是否属于管理员
    其包括：主人、群主、群管理
    """

    __slots__ = ()

    GROUP_ADMIN = ["admin", "owner"]

    async def __call__(self, bot: Bot, event: Event) -> bool:
        if isinstance(event, GroupMessageEvent):
            return event.sender.role in ["admin", "owner"] or is_master(bot, event)
        else:
            return False


init_permission()
MASTER = Permission(Master()).set_name("Master")
ADMIN = Permission(Admin()).set_name("Admin")
