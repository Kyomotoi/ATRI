import re
import json
from pathlib import Path
from types import ModuleType
from pydantic import BaseModel
from typing import List, Set, Tuple, Type, Union, Optional

from nonebot.matcher import Matcher
from nonebot.permission import Permission
from nonebot.dependencies import Dependent
from nonebot.typing import (
    T_State,
    T_Handler,
    T_RuleChecker,
    T_PermissionChecker,
)
from nonebot.rule import Rule, command, keyword, regex
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent

from ATRI.exceptions import ReadFileError, WriteFileError


SERVICES_DIR = Path(".") / "data" / "services"
SERVICES_DIR.mkdir(parents=True, exist_ok=True)


class ServiceInfo(BaseModel):
    service: str
    docs: str
    cmd_list: dict
    enabled: bool
    only_admin: bool
    disable_user: list
    disable_group: list


class CommandInfo(BaseModel):
    type: str
    docs: str
    aliases: Union[list, set]


class Service:
    """
    集成一套服务管理, 对功能信息持久化
    服务文件结构:
    {
        "service": "Service name",
        "docs": "Main helps and commands",
        "cmd_list": {
            "/cmd0": {
                "type": "Command type",
                "docs": "Command help",
                "aliases": ["More trigger ways."]
            }
        },
        "enabled": True,
        "only_admin": False,
        "disable_user": [],
        "disable_group": []
    }
    """

    def __init__(self, service: str):
        """初始化一个服务"""

        super().__init__()
        if not service:
            return

        self.service = service
        self._only_admin = False
        self._rule = is_in_service(service)
        self._permission = None
        self._handlers = None
        self._temp = False
        self._priority = 1
        self._state = None
        self._main_cmd = (str(),)

    def document(self, context: str) -> "Service":
        """为服务添加说明"""

        self.docs = context
        return self

    def only_admin(self, _is: bool) -> "Service":
        """标记服务仅管理员可用"""

        self._only_admin = _is
        return self

    def rule(self, rule: Optional[Union[Rule, T_RuleChecker]]) -> "Service":
        """为服务添加触发判定"""

        self._rule = self._rule & rule
        return self

    def permission(self, perm: Optional[Permission]) -> "Service":
        """为服务添加权限判定"""

        self._permission = perm
        return self

    def handlers(self, hand: Optional[List[T_Handler]]) -> "Service":
        """为服务设置处理函数"""

        self._handlers = hand
        return self

    def temp(self, _is: bool) -> "Service":
        """设置是否为一次性服务"""

        self._temp = _is
        return self

    def priority(self, level: int) -> "Service":
        """为服务设置优先级等级"""

        self._priority = level
        return self

    def state(self, state: Optional[T_State]) -> "Service":
        """为服务设置处理类型"""

        self._state = state
        return self

    def main_cmd(self, cmd: str) -> "Service":
        """为服务命令设置前缀"""

        self._main_cmd = (cmd,)
        return self

    def __generate_service_config(self, service: str, docs: str = str()) -> None:
        path = SERVICES_DIR / f"{service}.json"
        data = ServiceInfo(
            service=service,
            docs=docs,
            cmd_list=dict(),
            enabled=True,
            only_admin=self._only_admin,
            disable_user=list(),
            disable_group=list(),
        )
        try:
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps(data.dict(), indent=4))
        except Exception:
            raise WriteFileError("Write service info failed!")

    def save_service(self, service_data: dict, service: str) -> None:
        if not service:
            service = self.service

        path = SERVICES_DIR / f"{service}.json"
        if not path.is_file():
            self.__generate_service_config(service, self.docs)

        with open(path, "w", encoding="utf-8") as w:
            w.write(json.dumps(service_data, indent=4))

    def load_service(self, service: str) -> dict:
        path = SERVICES_DIR / f"{service}.json"
        if not path.is_file():
            self.__generate_service_config(service, self.docs)

        try:
            data = json.loads(path.read_bytes())
        except Exception:
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps({}))
            self.__generate_service_config(service, self.docs)
            data = json.loads(path.read_bytes())
        return data

    def __save_cmds(self, cmds: dict) -> None:
        data = self.load_service(self.service)
        temp_data: dict = data["cmd_list"]
        temp_data.update(cmds)
        self.save_service(data, self.service)

    def __load_cmds(self) -> dict:
        path = SERVICES_DIR / f"{self.service}.json"
        if not path.is_file():
            self.__generate_service_config(self.service, self.docs)

        data = json.loads(path.read_bytes())
        return data["cmd_list"]

    def on_message(
        self,
        name: str = str(),
        docs: str = str(),
        rule: Optional[Union[Rule, T_RuleChecker]] = None,
        permission: Optional[Union[Permission, T_PermissionChecker]] = None,
        handlers: Optional[List[Union[T_Handler, Dependent]]] = None,
        block: bool = True,
        priority: int = 1,
        state: Optional[T_State] = None,
    ) -> Type[Matcher]:
        if not rule:
            rule = self._rule
        if not permission:
            permission = self._permission
        if not handlers:
            handlers = self._handlers
        if not state:
            state = self._state

        if name:
            cmd_list = self.__load_cmds()

            name = name + "-onmsg"

            cmd_list[name] = CommandInfo(
                type="message", docs=docs, aliases=list()
            ).dict()
            self.__save_cmds(cmd_list)

        matcher = Matcher.new(
            "message",
            Rule() & rule,
            Permission() | permission,
            module=ModuleType(self.service),
            temp=self._temp,
            priority=priority,
            block=block,
            handlers=handlers,
            default_state=state,
        )
        return matcher

    def on_notice(self, name: str, docs: str, block: bool = True) -> Type[Matcher]:
        cmd_list = self.__load_cmds()

        name = name + "-onntc"

        cmd_list[name] = CommandInfo(type="notice", docs=docs, aliases=list()).dict()
        self.__save_cmds(cmd_list)

        matcher = Matcher.new(
            "notice",
            Rule() & self._rule,
            Permission(),
            module=ModuleType(self.service),
            temp=self._temp,
            priority=self._priority,
            block=block,
            handlers=self._handlers,
            default_state=self._state,
        )
        return matcher

    def on_request(self, name: str, docs: str, block: bool = True) -> Type[Matcher]:
        cmd_list = self.__load_cmds()

        name = name + "-onreq"

        cmd_list[name] = CommandInfo(type="request", docs=docs, aliases=list()).dict()
        self.__save_cmds(cmd_list)

        matcher = Matcher.new(
            "request",
            Rule() & self._rule,
            Permission(),
            module=ModuleType(self.service),
            temp=self._temp,
            priority=self._priority,
            block=block,
            handlers=self._handlers,
            default_state=self._state,
        )
        return matcher

    def on_command(
        self,
        cmd: Union[str, Tuple[str, ...]],
        docs: str,
        rule: Optional[Union[Rule, T_RuleChecker]] = None,
        aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = None,
        **kwargs,
    ) -> Type[Matcher]:
        cmd_list = self.__load_cmds()
        if not rule:
            rule = self._rule
        if not aliases:
            aliases = set()

        if isinstance(cmd, tuple):
            cmd = ".".join(map(str, cmd))

        cmd_list[cmd] = CommandInfo(
            type="command", docs=docs, aliases=list(aliases)
        ).dict()
        self.__save_cmds(cmd_list)
        commands = set([cmd]) | (aliases or set())
        return self.on_message(rule=command(*commands) & rule, block=True, **kwargs)

    def on_keyword(
        self,
        keywords: Set[str],
        docs: str,
        rule: Optional[Union[Rule, T_RuleChecker]] = None,
        **kwargs,
    ) -> Type[Matcher]:
        if not rule:
            rule = self._rule

        name = list(keywords)[0] + "-onkw"

        cmd_list = self.__load_cmds()

        cmd_list[name] = CommandInfo(type="keyword", docs=docs, aliases=keywords).dict()
        self.__save_cmds(cmd_list)

        return self.on_message(rule=keyword(*keywords) & rule, **kwargs)

    def on_regex(
        self,
        pattern: str,
        docs: str,
        flags: Union[int, re.RegexFlag] = 0,
        rule: Optional[Union[Rule, T_RuleChecker]] = None,
        **kwargs,
    ) -> Type[Matcher]:
        if not rule:
            rule = self._rule

        cmd_list = self.__load_cmds()
        cmd_list[pattern] = CommandInfo(type="regex", docs=docs, aliases=list()).dict()
        self.__save_cmds(cmd_list)

        return self.on_message(rule=regex(pattern, flags) & rule, **kwargs)

    def cmd_as_group(self, cmd: str, docs: str, **kwargs) -> Type[Matcher]:
        sub_cmd = (cmd,) if isinstance(cmd, str) else cmd
        _cmd = self._main_cmd + sub_cmd

        if "aliases" in kwargs:
            del kwargs["aliases"]

        return self.on_command(_cmd, docs, **kwargs)


class ServiceTools:
    """针对服务的工具类"""

    @staticmethod
    def save_service(service_data: dict, service: str):
        path = SERVICES_DIR / f"{service}.json"
        if not path.is_file():
            raise ReadFileError(
                f"Can't find service file: {service}\n"
                "Please delete all file in data/service/services\n"
                "And reboot bot."
            )

        with open(path, "w", encoding="utf-8") as w:
            w.write(json.dumps(service_data, indent=4))

    @staticmethod
    def load_service(service: str) -> dict:
        path = SERVICES_DIR / f"{service}.json"
        if not path.is_file():
            raise ReadFileError(
                f"Can't find service file: {service}\n"
                "Please delete all file in data/service/services\n"
                "And reboot bot."
            )

        with open(path, "r", encoding="utf-8") as r:
            data = json.loads(r.read())
        return data

    @classmethod
    def auth_service(cls, service, user_id: str = str(), group_id: str = str()) -> bool:
        data = cls.load_service(service)

        auth_global = data.get("enabled", True)
        auth_user = data.get("disable_user", list())
        auth_group = data.get("disable_group", list())

        if user_id:
            if user_id in auth_user:
                return False

        if group_id:
            return False if group_id in auth_group else True

        return auth_global

    @classmethod
    def service_controller(cls, service: str, is_enabled: bool):
        data = cls.load_service(service)
        data["enabled"] = is_enabled
        cls.save_service(data, service)


def is_in_service(service: str) -> Rule:
    async def _is_in_service(bot: Bot, event: Event) -> bool:
        result = ServiceTools().auth_service(service)
        if not result:
            return False

        if isinstance(event, PrivateMessageEvent):
            user_id = event.get_user_id()
            result = ServiceTools().auth_service(service, user_id)
            return result
        elif isinstance(event, GroupMessageEvent):
            user_id = event.get_user_id()
            group_id = str(event.group_id)
            result = ServiceTools().auth_service(service, user_id, group_id)
            return result
        else:
            return True

    return Rule(_is_in_service)
