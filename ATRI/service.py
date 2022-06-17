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
    集成一套服务管理，对功能信息进行持久化
    服务文件结构：
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

    def __init__(
        self,
        service: str,
        docs: str,
        only_admin: bool = False,
        rule: Optional[Union[Rule, T_RuleChecker]] = None,
        permission: Optional[Permission] = None,
        handlers: Optional[List[T_Handler]] = None,
        temp: bool = False,
        priority: int = 1,
        state: Optional[T_State] = None,
        main_cmd: str = str(),
    ):
        self.service = service
        self.docs = docs
        self.only_admin = only_admin
        self.rule = rule
        self.permission = permission
        self.handlers = handlers
        self.temp = temp
        self.priority = priority
        self.state = state
        self.main_cmd = (main_cmd,)

    def _generate_service_config(self, service: str, docs: str = str()) -> None:
        path = SERVICES_DIR / f"{service}.json"
        data = ServiceInfo(
            service=service,
            docs=docs,
            cmd_list=dict(),
            enabled=True,
            only_admin=self.only_admin,
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
            self._generate_service_config(service, self.docs)

        with open(path, "w", encoding="utf-8") as w:
            w.write(json.dumps(service_data, indent=4))

    def load_service(self, service: str) -> dict:
        path = SERVICES_DIR / f"{service}.json"
        if not path.is_file():
            self._generate_service_config(service, self.docs)

        try:
            data = json.loads(path.read_bytes())
        except Exception:
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps({}))
            self._generate_service_config(service, self.docs)
            data = json.loads(path.read_bytes())
        return data

    def _save_cmds(self, cmds: dict) -> None:
        data = self.load_service(self.service)
        temp_data: dict = data["cmd_list"]
        temp_data.update(cmds)
        self.save_service(data, self.service)

    def _load_cmds(self) -> dict:
        path = SERVICES_DIR / f"{self.service}.json"
        if not path.is_file():
            self._generate_service_config(self.service, self.docs)

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
            rule = self.rule
        if not permission:
            permission = self.permission
        if not handlers:
            handlers = self.handlers
        if not state:
            state = self.state

        if name:
            cmd_list = self._load_cmds()

            name = name + "-onmsg"

            cmd_list[name] = CommandInfo(
                type="message", docs=docs, aliases=list()
            ).dict()
            self._save_cmds(cmd_list)

        matcher = Matcher.new(
            "message",
            Rule() & rule,
            Permission() | permission,
            module=ModuleType(self.service),
            temp=self.temp,
            priority=priority,
            block=block,
            handlers=handlers,
            default_state=state,
        )
        return matcher

    def on_notice(self, name: str, docs: str, block: bool = True) -> Type[Matcher]:
        cmd_list = self._load_cmds()

        name = name + "-onntc"

        cmd_list[name] = CommandInfo(type="notice", docs=docs, aliases=list()).dict()
        self._save_cmds(cmd_list)

        matcher = Matcher.new(
            "notice",
            Rule() & self.rule,
            Permission(),
            module=ModuleType(self.service),
            temp=self.temp,
            priority=self.priority,
            block=block,
            handlers=self.handlers,
            default_state=self.state,
        )
        return matcher

    def on_request(self, name: str, docs: str, block: bool = True) -> Type[Matcher]:
        cmd_list = self._load_cmds()

        name = name + "-onreq"

        cmd_list[name] = CommandInfo(type="request", docs=docs, aliases=list()).dict()
        self._save_cmds(cmd_list)

        matcher = Matcher.new(
            "request",
            Rule() & self.rule,
            Permission(),
            module=ModuleType(self.service),
            temp=self.temp,
            priority=self.priority,
            block=block,
            handlers=self.handlers,
            default_state=self.state,
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
        cmd_list = self._load_cmds()
        if not rule:
            rule = self.rule
        if not aliases:
            aliases = set()

        if isinstance(cmd, tuple):
            cmd = ".".join(map(str, cmd))

        cmd_list[cmd] = CommandInfo(
            type="command", docs=docs, aliases=list(aliases)
        ).dict()
        self._save_cmds(cmd_list)
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
            rule = self.rule

        name = list(keywords)[0] + "-onkw"

        cmd_list = self._load_cmds()

        cmd_list[name] = CommandInfo(type="keyword", docs=docs, aliases=keywords).dict()
        self._save_cmds(cmd_list)

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
            rule = self.rule

        cmd_list = self._load_cmds()
        cmd_list[pattern] = CommandInfo(type="regex", docs=docs, aliases=list()).dict()
        self._save_cmds(cmd_list)

        return self.on_message(rule=regex(pattern, flags) & rule, **kwargs)

    def cmd_as_group(self, cmd: str, docs: str, **kwargs) -> Type[Matcher]:
        sub_cmd = (cmd,) if isinstance(cmd, str) else cmd
        _cmd = self.main_cmd + sub_cmd

        if "aliases" in kwargs:
            del kwargs["aliases"]

        return self.on_command(_cmd, docs, **kwargs)


class ServiceTools(object):
    @staticmethod
    def save_service(service_data: dict, service: str) -> None:
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
            if group_id in auth_group:
                return False
            else:
                return True

        if not auth_global:
            return False
        else:
            return True
