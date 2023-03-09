import os
import asyncio
from typing import Union
from datetime import datetime

from fastapi import APIRouter, status, Depends, Query, HTTPException
from fastapi.websockets import WebSocket, WebSocketState
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

from ATRI.utils import machine
from ATRI.service import SERVICES_DIR, ServiceInfo, ServiceTools

from ..data_source import *
from ..listener import get_message_info
from . import models


def _author(token: Union[str, None] = Query(default=None)):
    data = AuthDealer.get()
    if data is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="缺少信息")

    now_time = datetime.now().timestamp()
    if token != data.token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="密钥不正确")
    elif now_time > data.dead_time:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="密钥已过期")
    else:
        return "OK"


router = APIRouter(tags=["capi"], dependencies=[Depends(_author)])


@router.get("/", response_model=models.Response)
async def _():
    return models.Response(status=status.HTTP_200_OK, detail="控制台 API 路径", data=dict())


@router.get("/auth", response_model=models.Response)
async def _():
    return models.Response(status=status.HTTP_200_OK, detail="OK", data=dict())


@router.websocket("/status")
async def _(websocket: WebSocket):
    await websocket.accept()

    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_json(
                models.Response(
                    status=status.HTTP_200_OK,
                    detail="OK",
                    data=models.StatusInfo(
                        platform=machine.get_platform_info().dict(),
                        cpu=machine.get_cpu_info().dict(),
                        mem=machine.get_mem_info().dict(),
                        disk=machine.get_disk_info().dict(),
                        net=machine.get_net_info().dict(),
                    ).dict(),
                ).dict()
            )
            await asyncio.sleep(2)
    except ConnectionClosedOK:
        pass
    except ConnectionClosedError:
        pass
    finally:
        await websocket.close()
    return


@router.websocket("/status/message")
async def _(websocket: WebSocket):
    await websocket.accept()

    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_json(
                models.Response(
                    status=status.HTTP_200_OK,
                    detail="OK",
                    data=get_message_info().dict(),
                ).dict()
            )
            await asyncio.sleep(1)
    except ConnectionClosedOK:
        pass
    except ConnectionClosedError:
        pass
    finally:
        await websocket.close()
    return


@router.get("/service/list", response_model=models.Response)
async def _():
    result = dict()
    files = os.listdir(SERVICES_DIR)
    for f in files:
        if f == ".DS_Store":
            continue
        serv_path = SERVICES_DIR / f
        data = ServiceInfo.parse_file(serv_path)
        result[data.service] = data.dict()

    return models.Response(status=status.HTTP_200_OK, detail="OK", data=result)


@router.get("/service/edit", response_model=models.Response)
async def _(
    service: str,
    enabled: int,
    for_global: int = 1,
    user_id: int = int(),
    group_id: int = int(),
):
    msg = "OK"
    data = ServiceTools(service).load_service()
    if enabled and for_global:
        data.enabled = True
    elif not enabled and for_global:
        data.enabled = False

    if user_id or group_id:
        if enabled:
            if user_id not in data.disable_user:
                msg = "用户不存在于禁用名单"
            else:
                data.disable_user.remove(user_id)

            if group_id not in data.disable_group:
                msg = "群不存在于禁用名单"
            else:
                data.disable_group.remove(group_id)
        else:
            if user_id in data.disable_user:
                msg = "用户已存在于禁用名单"
            else:
                data.disable_user.append(user_id)

            if group_id in data.disable_group:
                msg = "群已存在于禁用名单"
            else:
                data.disable_group.append(group_id)

    ServiceTools(service).save_service(data.dict())

    return models.Response(status=status.HTTP_200_OK, detail=msg, data=dict())


def _get_block_list():
    # 该处有一 typo
    file_dir = Path(".") / "data" / "plugins" / "manege"
    path = file_dir / "block_user.json"
    user_data = json.loads(path.read_bytes())

    path = file_dir / "block_group.json"
    group_data = json.loads(path.read_bytes())

    return {"user": user_data, "group": group_data}


@router.get("/block/list", response_model=models.Response)
async def _():
    return models.Response(
        status=status.HTTP_200_OK, detail="OK", data=_get_block_list()
    )


@router.get("/block/edit", response_model=models.Response)
async def _(enabled: int, user_id: int = int(), group_id: int = int()):
    data = _get_block_list()
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = "OK"
    if enabled:
        if user_id:
            if user_id in data["user"]:
                msg = "用户已存在于黑名单"
            else:
                data["user"][user_id] = now_time
        if group_id:
            if group_id in data["group"]:
                msg = "群已存在于黑名单"
            else:
                data["group"][group_id] = now_time
    else:
        if user_id:
            if user_id not in data["user"]:
                msg = "用户不存在于黑名单"
            else:
                del data["user"][user_id]
        if group_id:
            if group_id not in data["group"]:
                msg = "群不存在于黑名单"
            else:
                del data["group"][group_id]

    file_dir = Path(".") / "data" / "plugins" / "manege"
    path = file_dir / "block_user.json"
    await FileDealer(path).write(json.dumps(data["user"]))

    path = file_dir / "block_group.json"
    await FileDealer(path).write(json.dumps(data["group"]))

    return models.Response(
        status=status.HTTP_200_OK,
        detail=msg,
        data=data,
    )
