from ..data_source import Status
from ..listener import get_message_deal_info


def handle_base_uri():
    return {"status": 204, "msg": "This path just for console load."}


def handle_runtime_info(token: str):
    auth, data = auth_token(token)
    plat, bot = Status().get_status(True)
    if auth:
        return {"status": 200, "data": {"platform": plat, "bot": bot}}
    else:
        return data


def handle_message_deal_info(token: str):
    auth, data = auth_token(token)
    if auth:
        return {"status": 200, "data": get_message_deal_info()}
    else:
        return data


def handle_auther(token: str):
    auth, data = auth_token(token)
    return data if auth else data


def auth_token(token: str) -> tuple:
    auth_data: dict = Status().get_auth_info()
    if not auth_data.get("token", None):
        return False, {"status": 500, "msg": "This bot is not create auth data yet."}
    _token = auth_data["token"]
    if token != _token:
        return False, {"status": 403, "msg": "Token error, please check again."}
    else:
        return True, {"status": 200, "msg": "OK"}
