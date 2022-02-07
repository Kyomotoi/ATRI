from nonebot.adapters.onebot.v11 import MessageEvent

from .data_source import Helper


main_help = Helper().on_command("菜单", "获取食用bot的方法", aliases={"menu"})


@main_help.handle()
async def _main_help():
    repo = Helper().menu()
    await main_help.finish(repo)


about_me = Helper().on_command("关于", "获取关于bot的信息", aliases={"about"})


@about_me.handle()
async def _about_me():
    repo = Helper().about()
    await about_me.finish(repo)


service_list = Helper().on_command("服务列表", "查看所有可用服务", aliases={"功能列表"})


@service_list.handle()
async def _service_list():
    repo = Helper().service_list()
    await service_list.finish(repo)


service_info = Helper().on_command("帮助", "获取服务详细帮助", aliases={"help"})


@service_info.handle()
async def _ready_service_info(event: MessageEvent):
    msg = str(event.get_message()).split(" ")

    try:
        service = msg[1]
    except:
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
