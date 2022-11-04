from nonebot.drivers.fastapi import Driver

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from ATRI import conf
from ATRI.log import log

from .path import *
from .api import *

from ..data_source import FRONTEND_DIR


def register_driver(driver: Driver):
    app = driver.server_app

    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )

    app.get(CONSOLE_BASE_URL)(base_url)

    app.get(CONSOLE_AUTH_URL)(auth_info)

    app.websocket(CONSOLE_RUNTIME_INFO_URL)(runtime_info)
    app.websocket(CONSOLE_MESSAGE_INFO_URL)(message_info)

    app.get(CONSOLE_SERVICE_LIST_URL)(service_list)
    app.get(CONSOLE_SERVICE_EDIT_URL)(edit_service)

    app.get(CONSOLE_BLOCK_LIST_URL)(block_list_info)
    app.get(CONSOLE_BLOCK_EDIT_URL)(edit_block_list)

    static_path = str(FRONTEND_DIR)
    app.mount(
        "/",
        StaticFiles(directory=static_path, html=True),
        name="atri-console",
    )


def init_driver():
    from ATRI import driver

    register_driver(driver())  # type: ignore
    c_url = f"{conf.BotConfig.host}:{conf.BotConfig.port}"
    log.success(f"控制台将运行于: http://{c_url} 对应API节点为: /capi")
