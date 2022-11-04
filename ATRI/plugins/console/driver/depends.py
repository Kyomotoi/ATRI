from typing import Union
from datetime import datetime

from fastapi import Query, HTTPException, status
from starlette.websockets import WebSocket

from ..data_source import AuthDealer


def http_author(token: Union[str, None] = Query(default=None)):
    data = AuthDealer.get()
    if data is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="验证信息不存在")

    now_time = datetime.now().timestamp()
    if token != data.token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="密钥不匹配, 请检查")
    elif now_time > data.dead_time:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="密钥已过期")
    else:
        return token


async def websocket_author(
    websocket: WebSocket, token: Union[str, None] = Query(default=None)
):
    data = AuthDealer.get()
    if not data:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    now_time = datetime.now().timestamp()
    if token != data.token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    elif now_time > data.dead_time:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    else:
        return token
