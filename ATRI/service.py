import os
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
from nonebot.typing import T_State, T_Handler, T_RuleChecker
from nonebot.rule import Rule, command, keyword

from .log import logger as log
from .config import config
from .utils.request import post_bytes

if TYPE_CHECKING:
    from nonebot.adapters import Bot, Event


SERVICE_DIR = Path('.') / 'ATRI' / 'data' / 'service'
SERVICES_DIR = SERVICE_DIR / 'services'
os.makedirs(SERVICE_DIR, exist_ok=True)
os.makedirs(SERVICES_DIR, exist_ok=True)


matcher_list: list = []
is_sleep: bool = False


def _load_block_list() -> dict:
    file_name = "ban.json"
    file = SERVICE_DIR / file_name
    try:
        data = json.loads(file.read_bytes())
    except:
        data = {
            "user": [],
            "group": []
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
    file_name = service + ".json"
    file = SERVICES_DIR / file_name
    try:
        data = json.loads(file.read_bytes())
    except:
        service_info = {
            "name": service,
            "docs": docs,
            "disable_user": _load_block_list()['user'],
            "disable_group": _load_block_list()['group']
        }
        with open(file, "w") as r:
            r.write(json.dumps(service_info, indent=4))
        data = service_info
    return data


def _save_service_config(service: str, data: dict) -> None:
    file_name = service + ".json"
    file = SERVICES_DIR / file_name
    with open(file, "w") as r:
        r.write(json.dumps(data, indent=4))


class Service:
    """
    集成一套服务管理，block准确至个人
    计划搭配前端使用
    """
    @staticmethod
    def manual_reg_service(service: str):
        file_name = service + ".json"
        file = SERVICES_DIR / file_name
        service_info = {
            "name": service,
            "docs": None,
            "disable_user": _load_block_list()['user'],
            "disable_group": _load_block_list()['group']
        }
        with open(file, "w") as r:
            r.write(json.dumps(service_info, indent=4))
    
    @staticmethod
    def auth_service(service: str, group: Optional[int] = None) -> bool:
        data = _load_service_config(service)
        return False if group in data["disable_group"] else True
    
    @staticmethod
    def control_service(service: str, group: int, is_enable: bool) -> None:
        data = _load_service_config(service)
        sv_group = data.get('disable_group', [])
        if is_enable:
            sv_group.remove(group)
            log.info(f"Service {service} has been enabled.")
        else:
            sv_group.append(group)
            log.info(f"Service {service} has been disabled.")
        data["disable_group"] = sv_group
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
    def on_notice(name: str,
                  docs: Optional[str] = None,
                  rule: Optional[Union[Rule, T_RuleChecker]] = None,
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
        _load_service_config(name, docs)
        matcher_list.append(name)
        return matcher

    @staticmethod
    def on_request(name: str,
                   docs: Optional[str] = None,
                   rule: Optional[Union[Rule, T_RuleChecker]] = None,
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
        _load_service_config(name, docs)
        matcher_list.append(name)
        return matcher

    @classmethod
    def on_command(cls,
                   name: str,
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
        _load_service_config(name, docs)
        matcher_list.append(name)
        return cls.on_message(command(*commands) & rule,
                              handlers=handlers, **kwargs)

    @classmethod
    def on_keyword(cls,
                   name: str,
                   keywords: Set[str],
                   docs: Optional[str] = None,
                   rule: Optional[Union[Rule, T_RuleChecker]] = None,
                   **kwargs) -> Type[Matcher]:
        _load_service_config(name, docs)
        matcher_list.append(name)
        return cls.on_message(keyword(*keywords) & rule, **kwargs)
    
    
    class NetworkPost:
        URL = (
            f"http://{config['NetworkPost']['host']}:"
            f"{config['NetworkPost']['port']}/"
        )
        
        @classmethod
        async def send_private_msg(cls,
                                user_id: int,
                                message: str,
                                auto_escape: bool = False): # -> Dict[str, Any]
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
        def send_msg(cls,
                    message_type: Optional[str] = ...,
                    user_id: Optional[int] = ...,
                    group_id: Optional[int] = ...,
                    message = Union[str],
                    auto_escape: bool = ...) -> Dict[str, Any]:
            ...

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
        
        @classmethod
        def auth_user(cls, user: int) -> bool:
            return False if user in _load_block_list()['user'] else True
        
        @staticmethod
        def auth_group(group: int) -> bool:
            return False if group in _load_block_list()['group'] else True
        
        @classmethod
        def control_list(cls,
                         is_enable: bool,
                         user: Optional[int] = None,
                         group: Optional[int] = None) -> None:
            data = _load_block_list()
            if user:
                if is_enable:
                    data['user'][user] = datetime.now().__str__
                    log.info(f"New blocked user: {user} | Time: {datetime.now()}")
                else:
                    del data[user]
                    log.info(f"User {user} has been unblock.")
            elif group:
                if is_enable:
                    data['group'][group] = datetime.now().__str__
                    log.info(f"New blocked group: {group} | Time: {datetime.now()}")
                else:
                    del data[user]
                    log.info(f"Group {group} has been unblock.")
            
            with open(cls.path, "w") as r:
                json.dump(data, r)
