from nonebot.adapters.onebot.v11 import MessageEvent

from ATRI.service import Service
from ATRI.rule import to_bot

from .data_source import Helper


plugin = Service("帮助").document("bot的食用指南~").rule(to_bot())


menu = plugin.on_command("菜单", "获取食用bot的方法", aliases={"menu"})


@menu.handle()
async def _():
    await menu.finish(Helper().menu())


about = plugin.on_command("关于", "获取关于bot的信息", aliases={"about"})


@about.handle()
async def _():
    await about.finish(Helper().about())


service_list = plugin.on_command("服务列表", "获取服务列表", aliases={"功能列表"})


@service_list.handle()
async def _():
    await service_list.finish(Helper().service_list())


service_info = plugin.on_command("帮助", "获取对应服务详细信息", aliases={"help"})


@service_info.handle()
async def _ready_service_info(event: MessageEvent):
    msg = str(event.get_message()).split(" ")

    try:
        service = msg[1]
    except Exception:
        service = "idk"

    try:
        cmd = msg[2]
    except Exception:
        cmd = None

    if not cmd:
        repo = Helper().service_info(service)
        await service_info.finish(repo)

    repo = Helper().cmd_info(service, cmd)
    await service_info.finish(repo)
