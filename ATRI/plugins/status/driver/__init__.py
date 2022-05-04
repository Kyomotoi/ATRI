from nonebot import get_driver
from nonebot.drivers.fastapi import Driver

from fastapi.middleware.cors import CORSMiddleware

from .view import (
    handle_auther,
    handle_base_uri,
    handle_runtime_info,
    handle_message_deal_info,
)


CONSOLE_API_URI = "/capi"  # base point
CONSOLE_API_AUTH_URI = "/capi/auth"  # 验证后台许可
CONSOLE_API_RUNTIME_URI = "/capi/runtime"  # 获取运行占用信息
CONSOLE_API_MESSAGE_URI = "/capi/message"
# CONSOLE_API_AUTH_COOKIES_URI = "/capi/auth/cookies"  # 验证cookies


def register_routes(driver: Driver):
    app = driver.server_app

    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.get(CONSOLE_API_URI)(handle_base_uri)
    app.get(CONSOLE_API_RUNTIME_URI)(handle_runtime_info)
    app.get(CONSOLE_API_MESSAGE_URI)(handle_message_deal_info)
    app.get(CONSOLE_API_AUTH_URI)(handle_auther)


def init():
    driver = get_driver()
    register_routes(driver)  # type: ignore
