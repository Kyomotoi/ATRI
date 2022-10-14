from nonebot.drivers.fastapi import Driver

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from ATRI import conf
from ATRI.log import log
from ATRI.plugins.console.data_source import FRONTEND_DIR
from .view import (
    handle_auther,
    handle_base_uri,
    handle_control_service,
    handle_edit_block,
    handle_get_block_list,
    handle_get_service_list,
    handle_runtime_info,
    handle_message_deal_info,
)


CONSOLE_API_URI = "/capi"  # base point
CONSOLE_API_AUTH_URI = "/capi/auth"  # 验证后台许可
CONSOLE_API_RUNTIME_URI = "/capi/runtime"  # 获取运行占用信息
CONSOLE_API_MESSAGE_URI = "/capi/message"  # 获取信息处理信息

CONSOLE_API_SERVICE_LIST_URI = "/capi/service/list"  # 获取服务列表
CONSOLE_API_SERVICE_CONTROL_URI = "/capi/service/control"  # 对服务作出修改

CONSOLE_API_BLOCK_LIST_URI = "/capi/block/list"  # 获取封禁列表
CONSOLE_API_BLOCK_EDIT_URI = "/capi/block/edit"  # 编辑封禁列表


def register_routes(driver: Driver):
    app = driver.server_app

    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )

    app.get(CONSOLE_API_URI)(handle_base_uri)
    app.get(CONSOLE_API_AUTH_URI)(handle_auther)
    app.get(CONSOLE_API_RUNTIME_URI)(handle_runtime_info)
    app.get(CONSOLE_API_MESSAGE_URI)(handle_message_deal_info)

    app.get(CONSOLE_API_SERVICE_LIST_URI)(handle_get_service_list)
    app.get(CONSOLE_API_SERVICE_CONTROL_URI)(handle_control_service)

    app.get(CONSOLE_API_BLOCK_LIST_URI)(handle_get_block_list)
    app.get(CONSOLE_API_BLOCK_EDIT_URI)(handle_edit_block)

    static_path = str(FRONTEND_DIR)
    app.mount(
        "/",
        StaticFiles(directory=static_path, html=True),
        name="atri-console",
    )


def init_driver():
    from ATRI import driver

    c_url = f"{conf.BotConfig.host}:{conf.BotConfig.port}"
    log.info(f"控制台将运行于: http://{c_url} 对应API节点为: /capi")
    register_routes(driver())  # type: ignore
