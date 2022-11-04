import asyncio

from fastapi import Depends, status
from starlette.websockets import WebSocket, WebSocketState
from websockets.exceptions import ConnectionClosedOK

from .depends import *
from .data_source import (
    get_process_info,
    get_service_list,
    edit_service as _edit_service,
    get_block_list,
    edit_block_list as _edit_block_list,
)
from ..listener import get_message_info


def base_url(_=Depends(http_author)):
    return {"status": status.HTTP_204_NO_CONTENT, "msg": "该路径仅供控制台加载"}


def auth_info(_=Depends(http_author)):
    return {"status": status.HTTP_200_OK, "detail": "OK"}


async def runtime_info(websocket: WebSocket, _pass=Depends(websocket_author)):
    if not _pass:
        return
    await websocket.accept()

    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_json(get_process_info())
            await asyncio.sleep(1)
    except ConnectionClosedOK:
        pass
    finally:
        await websocket.close()
    return


async def message_info(websocket: WebSocket, _pass=Depends(websocket_author)):
    if not _pass:
        return
    await websocket.accept()

    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_json(get_message_info())
            await asyncio.sleep(1)
    except ConnectionClosedOK:
        pass
    finally:
        await websocket.close()
    return


def service_list(_=Depends(http_author)):
    return {"status": status.HTTP_200_OK, "data": get_service_list()}


def edit_service(
    service: str,
    global_enabled: str = "2",
    enabled: str = "2",
    user: str = str(),
    group: str = str(),
    _=Depends(http_author),
):
    return {
        "status": status.HTTP_200_OK,
        "data": _edit_service(
            service, int(global_enabled), bool(int(enabled)), user, group
        ),
    }


def block_list_info(_=Depends(http_author)):
    return {"status": status.HTTP_200_OK, "data": get_block_list()}


def edit_block_list(enabled: str, user_id: str = str(), group_id: str = str(), _=Depends(http_author)):
    return {
        "status": status.HTTP_200_OK,
        "data": _edit_block_list(bool(int(enabled)), user_id, group_id),
    }
