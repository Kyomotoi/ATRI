import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import (
    Dict,
    Any,
    List,
    Set,
    Tuple,
    Type,
    Union,
    Optional,
    TYPE_CHECKING
)
from nonebot.matcher import Matcher
from nonebot.permission import Permission
from nonebot.plugin import on_message
from nonebot.typing import T_State, T_Handler, T_RuleChecker
from nonebot.rule import Rule, command, keyword, regex

from .log import logger as log
from .config import Config
from .utils.request import post_bytes

if TYPE_CHECKING:
    from nonebot.adapters import Bot, Event


SERVICE_DIR = Path('.') / 'ATRI' / 'data' / 'service'
SERVICES_DIR = SERVICE_DIR / 'services'
os.makedirs(SERVICE_DIR, exist_ok=True)
os.makedirs(SERVICES_DIR, exist_ok=True)


is_sleep: bool = False
matcher_list: list = []


def _load_block_list() -> dict:
    file_name = "ban.json"
    file = SERVICE_DIR / file_name
    try:
        data = json.loads(file.read_bytes())
    except:
        data = {
            "user": {},
            "group": {}
        }
        with open(file, "w") as r:
            r.write(json.dumps(data, indent=4))
    return data


def _save_block_list(data: dict) -> None:
    file_name = "ban.json"
    file = SERVICE_DIR / file_name
    with open(file, "w") as r:
        r.write(json.dumps(data, indent=4))


def _load_service_config(service: str, docs: str = None) -> dict:
    file_name = service.replace('/', '') + ".json"
    file = SERVICES_DIR / file_name
    try:
        data = json.loads(file.read_bytes())
    except:
        service_info = {
            "command": service,
            "docs": docs,
            "enabled": True,
            "disable_user": {},
            "disable_group": {}
        }
        with open(file, "w") as r:
            r.write(json.dumps(service_info, indent=4))
        data = service_info
    return data


def _save_service_config(service: str, data: dict) -> None:
    file_name = service.replace('/', '') + ".json"
    file = SERVICES_DIR / file_name
    with open(file, "w") as r:
        r.write(json.dumps(data, indent=4))


class Service:
    """
    集成一套服务管理，对功能信息进行持久化
    计划搭配前端使用
    """
    @staticmethod
    def manual_reg_service(service: str, docs: str = None):
        file_name = service.replace('/', '') + ".json"
        file = SERVICES_DIR / file_name
        service_info = {
            "command": service,
            "docs": docs,
            "enabled": True,
            "disable_user": {},
            "disable_group": {}
        }
        with open(file, "w") as r:
            r.write(json.dumps(service_info, indent=4))
    
    @staticmethod
    def auth_service(service: str, user: str, group: str = None) -> bool:
        data = _load_service_config(service)
        if user in data["disable_user"]:
            return False
        else:
            if group in data["disable_group"]:
                return False
            else:
                return True
    
    @staticmethod
    def control_service(service: str,
                        is_global: bool,
                        is_enabled: int,
                        user: str = None,
                        group: str = None) -> None:
        data = _load_service_config(service)
        is_enabled = bool(is_enabled)
        
        if is_global:
            status = "disabled" if is_enabled else "enabled"
            data['enabled'] = is_enabled
            log.info(f"\033[33mService: {service} has been {status}.\033[33m")
        else:
            if user:
                if not is_enabled:
                    data['disable_user'][user] = str(datetime.now())
                    log.info(f"\033[33mNew service blocked user: {user}\033[33m"
                             f"\033[33m | Service: {service} | Time: {datetime.now()}\033[33m")
                else:
                    if user in data['disable_user']:
                        del data['disable_user'][user]
                        log.info(f"\033[33mUser: {user} has been unblock\033[33m"
                                f"\033[33m | Service: {service} | Time: {datetime.now()}\033[33m")
            else:
                if not is_enabled:
                    data['disable_group'][group] = str(datetime.now())
                    log.info(f"\033[33mNew service blocked group: {group}\033[33m"
                             f"\033[33m | Service: {service} | Time: {datetime.now()}\033[33m")
                else:
                    if group in data['disable_group']:
                        del data['disable_group'][group]
                        log.info(f"\033[33mGroup: {group} has been unblock\033[33m"
                                f"\033[33m | Service: {service} | Time: {datetime.now()}\033[33m")
        _save_service_config(service, data)
    
    @staticmethod
    def on_message(rule: Optional[Union[Rule, T_RuleChecker]] = None,
                   permission: Optional[Permission] = None,
                   *,
                   handlers: Optional[List[T_Handler]] = None,
                   temp: bool = False,
                   priority: int = 1,
                   block: bool = True,
                   state: Optional[T_State] = None) -> Type[Matcher]:
        matcher = Matcher.new("message",
                              Rule() & rule,
                              permission or Permission(),
                              temp=temp,
                              priority=priority,
                              block=block,
                              handlers=handlers,
                              default_state=state)
        return matcher

    @staticmethod
    def on_notice(rule: Optional[Union[Rule, T_RuleChecker]] = None,
                  *,
                  handlers: Optional[List[T_Handler]] = None,
                  temp: bool = False,
                  priority: int = 1,
                  block: bool = False,
                  state: Optional[T_State] = None) -> Type[Matcher]:
        matcher = Matcher.new("notice",
                              Rule() & rule,
                              Permission(),
                              temp=temp,
                              priority=priority,
                              block=block,
                              handlers=handlers,
                              default_state=state)
        return matcher

    @staticmethod
    def on_request(rule: Optional[Union[Rule, T_RuleChecker]] = None,
                   *,
                   handlers: Optional[List[T_Handler]] = None,
                   temp: bool = False,
                   priority: int = 1,
                   block: bool = False,
                   state: Optional[T_State] = None) -> Type[Matcher]:
        matcher = Matcher.new("request",
                              Rule() & rule,
                              Permission(),
                              temp=temp,
                              priority=priority,
                              block=block,
                              handlers=handlers,
                              default_state=state)
        return matcher

    @classmethod
    def on_command(cls,
                   cmd: Union[str, Tuple[str, ...]],
                   docs: Optional[str] = None,
                   rule: Optional[Union[Rule, T_RuleChecker]] = None,
                   aliases: Optional[Set[Union[str, Tuple[str, ...]]]] = None,
                   **kwargs) -> Type[Matcher]:
        async def _strip_cmd(bot: "Bot", event: "Event", state: T_State):
            message = event.get_message()
            segment = message.pop(0)
            new_message = message.__class__(
                str(segment).lstrip()
                [len(state["_prefix"]["raw_command"]):].lstrip())  # type: ignore
            for new_segment in reversed(new_message):
                message.insert(0, new_segment)
        
        handlers = kwargs.pop("handlers", [])
        handlers.insert(0, _strip_cmd)
        
        commands = set([cmd]) | (aliases or set())
        _load_service_config(str(cmd), docs)
        return cls.on_message(command(*commands) & rule,
                              handlers=handlers, **kwargs)

    @classmethod
    def on_keyword(cls,
                   keywords: Set[str],
                   docs: Optional[str] = None,
                   rule: Optional[Union[Rule, T_RuleChecker]] = None,
                   **kwargs) -> Type[Matcher]:
        _load_service_config(list(keywords)[0], docs)
        return cls.on_message(keyword(*keywords) & rule, **kwargs)
    
    @classmethod
    def on_regex(cls,
                 pattern: str,
                 flags: Union[int, re.RegexFlag] = 0,
                 rule: Optional[Union[Rule, T_RuleChecker]] = None,
                 **kwargs) -> Type[Matcher]:
        return on_message(regex(pattern, flags) & rule, **kwargs)
    
    
    class NetworkPost:
        URL = (
            f"http://{Config.NetworkPost.host}:"
            f"{Config.NetworkPost.port}/"
        )
        
        @classmethod
        async def send_private_msg(cls,
                                user_id: int,
                                message: str,
                                auto_escape: bool = False) -> Dict[str, Any]:
            url = cls.URL + "send_private_msg?"
            params = {
                "user_id": user_id,
                "message": message,
                "auto_escape": f"{auto_escape}"
            }
            result = json.loads(await post_bytes(url, params))
            log.debug(result)
            return result

        @classmethod
        def send_group_msg(cls,
                        group_id: int,
                        message: Union[str],
                        auto_escape: Optional[bool] = ...) -> Dict[str, Any]:
            ...

        @classmethod
        async def send_msg(cls,
                    message_type: Optional[str] = "",
                    user_id: Optional[int] = None,
                    group_id: Optional[int] = None,
                    message = Union[str],
                    auto_escape: bool = False) -> Dict[str, Any]:
            url = cls.URL + "send_msg?"
            params = {
                "message_type": "",
                "user_id": user_id,
                "group_id": group_id,
                "message": message,
                "auto_escape": str(auto_escape)
            }
            result = json.loads(await post_bytes(url, params))
            log.debug(result)
            return result

        @classmethod
        def delete_msg(cls,
                    message_id: int):
            ...

        @classmethod
        def get_msg(cls,
                    message_id: int) -> Dict[str, Any]:
            ...

        @classmethod
        def get_forward_msg(cls,
                            id: int):
            ...

        @classmethod
        def send_like(cls,
                    user_id: int,
                    times: int = ...):
            ...

        @classmethod
        def set_group_kick(cls,
                        group_id: int,
                        user_id: int,
                        reject_add_request: bool = ...):
            ...

        @classmethod
        def set_group_ban(cls,
                        group_id: int,
                        user_id: int,
                        duration: int = ...):
            ...

        @classmethod
        def set_group_anonymous_ban(cls,
                                    group_id: int,
                                    anonymous: Optional[Dict[str, Any]] = ...,
                                    flag: Optional[str] = ...,
                                    duration: int = ...):
            ...

        @classmethod
        def set_group_whole_ban(cls,
                                group_id: int,
                                enable: bool = ...):
            ...

        @classmethod
        def set_group_admin(cls,
                            group_id: int,
                            user_id: int,
                            enable: bool = ...):
            ...

        @classmethod
        def set_group_anonymous(cls,
                                group_id: int,
                                enable: bool = ...):
            ...
        
        @classmethod
        def set_group_card(cls):
            ...

        @classmethod
        def set_group_name(cls):
            ...
        
        @classmethod
        def set_group_leave(cls):
            ...
        
        @classmethod
        def set_group_special_title(cls):
            ...
        
        @classmethod
        def set_friend_add_request(cls):
            ...
        
        @classmethod
        def set_group_add_request(cls):
            ...

        @classmethod
        def get_login_info(cls):
            ...
        
        @classmethod
        def get_stranger_info(cls):
            ...
        
        @classmethod
        def get_friend_list(cls):
            ...
        
        @classmethod
        def get_group_info(cls):
            ...
        
        @classmethod
        def get_group_list(cls):
            ...
        
        @classmethod
        def get_group_member_info(cls):
            ...
        
        @classmethod
        def get_group_member_list(cls):
            ...

        @classmethod
        def get_group_honor_info(cls):
            ...
        
        @classmethod
        def get_cookies(cls):
            ...
        
        @classmethod
        def get_csrf_token(cls):
            ...
        
        @classmethod
        def get_credentials(cls):
            ...
        
        @classmethod
        def get_record(cls):
            ...
        
        @classmethod
        def get_image(cls):
            ...
        
        @classmethod
        def can_send_image(cls):
            ...
        
        @classmethod
        def can_send_record(cls):
            ...
        
        @classmethod
        def get_status(cls):
            ...
        
        @classmethod
        def get_version_info(cls):
            ...
        
        @classmethod
        def set_restart(cls):
            ...
        
        @classmethod
        def clean_cache(cls):
            ...
    
    
    class Dormant:
        @staticmethod
        def is_dormant() -> bool:
            return False if is_sleep else True
        
        @staticmethod
        def control_dormant(is_enable: bool) -> None:
            global is_sleep
            if is_enable:
                is_sleep = True
            else:
                is_sleep = False
    
    
    class BlockSystem:
        file_name = "ban.json"
        path = SERVICE_DIR / file_name
        
        @staticmethod
        def auth_user(user: str) -> bool:
            return False if user in _load_block_list()['user'] else True
        
        @staticmethod
        def auth_group(group: str) -> bool:
            return False if group in _load_block_list()['group'] else True
        
        @staticmethod
        def control_list(is_enabled: bool,
                         user: str = None,
                         group: str = None) -> None:
            data = _load_block_list()
            if user:
                if is_enabled:
                    data['user'][user] = str(datetime.now())
                    log.info(f"\033[33mNew blocked user: {user} | Time: {datetime.now()}\033[33m")
                else:
                    del data['user'][str(user)]
                    log.info(f"\033[33mUser {user} has been unblock.\033[33m")
            elif group:
                if is_enabled:
                    data['group'][group] = str(datetime.now())
                    log.info(f"\033[33mNew blocked group: {group} | Time: {datetime.now()}\033[33m")
                else:
                    del data['group'][str(group)]
                    log.info(f"\033[33mGroup {group} has been unblock.\033[33m")
            _save_block_list(data)
