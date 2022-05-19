from ..data_source import Console
from ..listener import get_message_deal_info
from .api import (
    control_service,
    edit_block_list,
    get_block_list,
    get_processing_data,
    get_service_list,
)


def auth_token(token: str) -> tuple:
    auth_data: dict = Console().get_auth_info()
    if not auth_data.get("token", None):
        return False, {"status": 500, "msg": "This bot is not create auth data yet."}
    _token = auth_data["token"]
    if token != _token:
        return False, {"status": 403, "msg": "Token error, please check again."}
    else:
        return True, {"status": 200, "msg": "OK"}


def handle_base_uri():
    return {"status": 204, "msg": "This path just for console load."}


def handle_auther(token: str):
    auth, data = auth_token(token)
    return data if auth else data


def handle_runtime_info(token: str):
    auth, data = auth_token(token)
    if not auth:
        return data

    plat, bot = get_processing_data()
    return {"status": 200, "data": {"platform": plat, "bot": bot}}


def handle_message_deal_info(token: str):
    auth, data = auth_token(token)
    if not auth:
        return data

    return {"status": 200, "data": get_message_deal_info()}


def handle_get_service_list(token: str):
    auth, data = auth_token(token)
    if not auth:
        return data

    return {"status": 200, "data": get_service_list()}


def handle_control_service(
    token: str,
    service: str,
    is_enabled: int = 1,
    enabled_user: str = str(),
    enabled_group: str = str(),
    disable_user: str = str(),
    disable_group: str = str(),
):
    auth, data = auth_token(token)
    if not auth:
        return data

    is_ok, data = control_service(
        service, is_enabled, enabled_user, enabled_group, disable_user, disable_group
    )
    if not is_ok:
        return {"status": 422, "msg": "Dealing service data failed"}

    return {"status": 200, "data": data}


def handle_get_block_list(token: str):
    auth, data = auth_token(token)
    if not auth:
        return data

    return {"status": 200, "data": get_block_list()}


def handle_edit_block(
    token: str,
    is_enabled: bool,
    user_id: str = str(),
    group_id: str = str(),
):
    auth, data = auth_token(token)
    if not auth:
        return data

    is_ok, data = edit_block_list(is_enabled, user_id, group_id)
    if not is_ok:
        return {"status": 422, "msg": "Dealing block data failed"}

    return {"status": 200, "data": data}
