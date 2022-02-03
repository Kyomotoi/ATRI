import pytest
from nonebug import App

from .utils import make_fake_message, make_fake_event


@pytest.mark.asyncio
async def test_main_help(app: App):
    from ATRI.plugins.help import main_help

    Message = make_fake_message()

    async with app.test_matcher(main_help) as ctx:
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
            """,
            True,
        )


@pytest.mark.asyncio
async def test_about_me(app: App):
    from ATRI import __version__
    from ATRI.config import BotSelfConfig
    from ATRI.plugins.help import about_me

    temp_list = list()
    for i in BotSelfConfig.nickname:
        temp_list.append(i)
    nickname = "、".join(map(str, temp_list))

    Message = make_fake_message()

    async with app.test_matcher(about_me) as ctx:
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
            https://github.com/Kyomotoi/ATRI
            """,
            True,
        )


@pytest.mark.asyncio
async def test_service_list(app: App):
    import os

    from ATRI.service import SERVICES_DIR
    from ATRI.plugins.help import service_list

    files = os.listdir(SERVICES_DIR)
    temp_list = list()
    for i in files:
        service = i.replace(".json", "")
        temp_list.append(service)

    services = "、".join(map(str, temp_list))

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
            {services}
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
        ctx.should_call_send(event, "请检查是否输入错误...", True)

    async with app.test_matcher(service_info) as ctx:
        bot = ctx.create_bot()

        msg = Message("帮助 状态")
        event = make_fake_event(_message=msg, _to_me=True)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            """
            服务名：状态
            说明：
            检查咱自身状态

            可用命令：
                /ping、/status
            是否全局启用：True
            Tip: 帮助 [服务] [命令] 以查看对应命令详细信息
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
