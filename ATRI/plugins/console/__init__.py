from datetime import datetime

from nonebot.params import ArgPlainText
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent

from ATRI import conf
from ATRI.log import log
from ATRI.service import Service
from ATRI.permission import MASTER
from ATRI.message import MessageBuilder
from ATRI.utils.apscheduler import scheduler

from .data_source import AuthDealer, get_host_ip


plugin = (
    Service("控制台")
    .document("前端管理页面")
    .only_admin(True)
    .permission(MASTER)
    .main_cmd("/con")
)


async def __del_auth_key():
    await AuthDealer.clear()
    log.warning("控制台验证密钥已过期")


gen_console_key = plugin.cmd_as_group("auth", "获取进入网页后台的凭证")


@gen_console_key.got("is_pub_n", "咱的运行环境是否有公网(y/n)")
async def _(event: PrivateMessageEvent, is_pub_n: str = ArgPlainText("is_pub_n")):
    is_access_key = conf.BotConfig.access_token
    if not is_access_key:
        await gen_console_key.finish(
            MessageBuilder("缺少设置: access_token")
            .text("请先填写该内容, 以保证ATRI与协议端链接的安全性")
            .text("填写并重启, 方可启用控制台")
            .text("Tip: 该内容请尽可能地复杂, 请勿使用中文")
        )

    auth_info = AuthDealer.get()
    if auth_info:
        now_time = datetime.now().timestamp()
        if now_time < auth_info.dead_time:
            raw_last_time = auth_info.dead_time - now_time
            last_time = datetime.fromtimestamp(raw_last_time).minute
            await gen_console_key.finish(
                MessageBuilder("之前生成的密钥还在有效时间内奥")
                .text(f"Token: {auth_info.token}")
                .text(f"剩余有效时间: {last_time} min")
            )
    await AuthDealer.clear()

    if is_pub_n != "y":
        host = str(await get_host_ip(False))
        await gen_console_key.send("没有公网吗...嗯知道了")
    else:
        host = str(await get_host_ip(True))
    port = conf.BotConfig.port
    auth = AuthDealer()
    data = await auth.store()

    msg = (
        MessageBuilder("控制台信息已生成!")
        .text(f"请访问: {host}:{port}")
        .text(f"Token: {auth.get_token()}")
        .text("该 token 有效时间为 15min")
    )

    scheduler.add_job(
        __del_auth_key,
        name="清除后台验证凭证",
        next_run_time=datetime.fromtimestamp(data.dead_time),
        misfire_grace_time=15,
    )

    await gen_console_key.finish(msg)


@gen_console_key.handle()
async def _(event: GroupMessageEvent):
    await gen_console_key.finish("请私戳咱获取（")


del_console_key = plugin.cmd_as_group("del", "销毁进入网页后台的凭证")


@del_console_key.got("is_sure_d", "...你确定吗(y/n)")
async def _(is_sure: str = ArgPlainText("is_sure_d")):
    if is_sure != "y":
        await del_console_key.finish("反悔了呢...")

    data = AuthDealer.get()
    if data is None:
        await del_console_key.finish("你还没向咱索取凭证呢...私戳咱键入 /con.auth 以获取")

    await AuthDealer.clear()

    await del_console_key.finish("销毁成功！如需再次获取: /con.auth")


from ATRI import driver as dr
from .data_source import init_resource
from .driver import init_driver


dr().on_startup(init_resource)
dr().on_startup(init_driver)
