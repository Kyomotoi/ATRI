import pytest
from nonebug import App

from .utils import make_fake_message, make_fake_event


@pytest.mark.asyncio
async def test_main_help(app: App):
    from ATRI.plugins.help import menu

    Message = make_fake_message()

    async with app.test_matcher(menu) as ctx:
        bot = ctx.create_bot()

        msg = Message("菜单")
        event = make_fake_event(_message=msg, _to_me=True)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            """
            哦呀？~需要帮助？
            关于 -查看bot基本信息
            服务列表 -以查看所有可用服务
            帮助 [服务] -以查看对应服务帮助
            Tip: 均需要at触发。@bot 菜单 以打开此页面
            """.strip(),
            True,
        )


@pytest.mark.asyncio
async def test_about_me(app: App):
    from ATRI import __version__, conf
    from ATRI.plugins.help import about

    temp_list = list()
    for i in conf.BotConfig.nickname:
        temp_list.append(i)
    nickname = "、".join(map(str, temp_list))

    Message = make_fake_message()

    async with app.test_matcher(about) as ctx:
        bot = ctx.create_bot()

        msg = Message("关于")
        event = make_fake_event(_message=msg, _to_me=True)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            f"""
            唔...是来认识咱的么
            可以称呼咱：{nickname}
            咱的型号是：{__version__}
            想进一步了解：
            atri.kyomotoi.moe
            进不去: project-atri-docs.vercel.app
            """.strip(),
            True,
        )


@pytest.mark.asyncio
async def test_service_list(app: App):
    import os
    import json
    from tabulate import tabulate

    from ATRI.service import SERVICES_DIR
    from ATRI.plugins.help import service_list

    files = os.listdir(SERVICES_DIR)
    services = list()
    for f in files:
        prefix = f.replace(".json", "")
        f = os.path.join(SERVICES_DIR, f)
        with open(f, "r", encoding="utf-8") as r:
            service = json.load(r)
            services.append(
                [
                    prefix,
                    "√" if service["enabled"] else "×",
                    "√" if service["only_admin"] else "×",
                ]
            )
    table = tabulate(
        services,
        headers=["服务名称", "开启状态(全局)", "仅支持管理员"],
        tablefmt="plain",
    )
    output = f"咱搭载了以下服务~\n{table}\n@bot 帮助 [服务] -以查看对应服务帮助"

    Message = make_fake_message()

    async with app.test_matcher(service_list) as ctx:
        bot = ctx.create_bot()

        msg = Message("服务列表")
        event = make_fake_event(_message=msg, _to_me=True)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            f"""
            咱搭载了以下服务~
            {output}
            @bot 帮助 [服务] -以查看对应服务帮助
            """,
            True,
        )


@pytest.mark.asyncio
async def test_service_info(app: App):
    from ATRI.plugins.help import service_info

    Message = make_fake_message()

    async with app.test_matcher(service_info) as ctx:
        bot = ctx.create_bot()

        msg = Message("帮助")
        event = make_fake_event(_message=msg, _to_me=True)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "请检查是否输入错误呢...@bot 帮助 [服务]", True)

    async with app.test_matcher(service_info) as ctx:
        bot = ctx.create_bot()

        msg = Message("帮助 状态")
        event = make_fake_event(_message=msg, _to_me=True)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            """
            服务名：状态
            说明：检查咱自身状态
            可用命令：
                /ping
                /status
            是否全局启用：True
            Tip: @bot 帮助 [服务] [命令] 以查看对应命令详细信息
            """,
            True,
        )

    async with app.test_matcher(service_info) as ctx:
        bot = ctx.create_bot()

        msg = Message("帮助 状态 /ping")
        event = make_fake_event(_message=msg, _to_me=True)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            """
            命令：/ping
            类型：command
            说明：检测bot简单信息处理速度
            更多触发方式：[]
            """,
            True,
        )
