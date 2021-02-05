'''
获取更多帮助 >> https://github.com/howmanybots/onebot/blob/master/v11/specs/api/public.md
'''
import json
from typing import (
    Optional,
    Union,
    Dict,
    Any
)

from ATRI.log import logger
from ATRI.config import config
from ATRI.utils.request import post_bytes


URL = (
    f"http://{config['HttpPost']['host']}:"
    f"{config['HttpPost']['port']}/"
)


class HttpPost:

    @classmethod
    async def send_private_msg(cls,
                               user_id: int,
                               message: str,
                               auto_escape: bool = False): # -> Dict[str, Any]
        url = URL + "send_private_msg?"
        params = {
            "user_id": user_id,
            "message": message,
            "auto_escape": f"{auto_escape}"
        }
        result = json.loads(await post_bytes(url, params))
        logger.debug(result)
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
