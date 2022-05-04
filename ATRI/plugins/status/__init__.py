import json

from nonebot.params import ArgPlainText
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent

from ATRI.log import logger as log
from ATRI.config import BotSelfConfig
from ATRI.exceptions import ReadFileError, WriteError
from ATRI.utils.apscheduler import scheduler
from .data_source import Status, STATUS_DIR
from .models import ForAuthData
from .driver import init

init()


ping = Status().on_command("/ping", "检测bot简单信息处理速度")


@ping.handle()
async def _ping():
    await ping.finish(Status.ping())


status = Status().on_command("/status", "查看运行资源占用")


@status.handle()
async def _status():
    msg, _ = Status.get_status()
    await status.finish(msg)


info_msg = "アトリは高性能ですから！"


@scheduler.scheduled_job("interval", name="状态检查", minutes=10, misfire_grace_time=15)  # type: ignore
async def _check_runtime():
    log.info("开始检查资源消耗...")
    msg, stat = Status().get_status()
    if not stat:
        await status.finish(msg)


get_console_key = Status().on_command("/auth", "获取进入网页后台的凭证", permission=SUPERUSER)


@get_console_key.got("is_pub_n", "咱的运行环境是否有公网(y/n)")
async def _(event: PrivateMessageEvent, is_pub_n: str = ArgPlainText("is_pub_n")):
    if is_pub_n != "y":
        ip = str(await Status().get_host_ip(False))
        await get_console_key.send("没有公网吗...嗯知道了")
    else:
        ip = str(await Status().get_host_ip(True))

    p = BotSelfConfig.port
    rs = Status().get_random_str(20)

    df = STATUS_DIR / "data.json"
    try:
        if not df.is_file():
            with open(df, "w", encoding="utf-8") as w:
                w.write(json.dumps({}))

        d = json.loads(df.read_bytes())

        ca = d.get("data", None)
        if ca:
            # 此处原本想用 matcher.finish 但这是在 try 里啊！
            await get_console_key.send("咱已经告诉你了嗷！啊！忘了.../gauth 获取吧")
            return

        d["data"] = ForAuthData(ip=ip, port=str(p), token=rs).dict()

        with open(df, "w", encoding="utf-8") as w:
            w.write(json.dumps(d))
    except WriteError:
        msg = f"""
        哦吼！写入文件失败了...还请自行记下哦...
        IP: {ip}
        PORT: {p}
        TOKEN: {rs}
        一定要保管好哦！切勿告诉他人哦！
        """.strip()
        await get_console_key.send(msg)

        raise WriteError("Writing file: " + str(df) + " failed!")

    msg = f"""
    该信息已保存！可通过 /gauth 获取~
    IP: {ip}
    PORT: {p}
    TOKEN: {rs}
    一定要保管好哦！切勿告诉他人哦！
    """.strip()
    await get_console_key.finish(msg)


@get_console_key.handle()
async def _(event: GroupMessageEvent):
    await get_console_key.finish("请私戳咱获取（")


load_console_key = Status().on_command("/gauth", "获取已生成的后台凭证", permission=SUPERUSER)


@load_console_key.handle()
async def _(event: PrivateMessageEvent):
    df = STATUS_DIR / "data.json"
    if not df.is_file():
        await load_console_key.finish("你还没有问咱索要奥！/auth 以获取")

    try:
        d = json.loads(df.read_bytes())
    except ReadFileError:
        await load_console_key.send("获取数据失败了...请自行打开文件查看吧:\n" + str(df))
        raise ReadFileError("Reading file: " + str(df) + " failed!")

    data = d["data"]
    msg = f"""
    诶嘿嘿嘿——凭证信息来咯！
    IP: {data['ip']}
    PORT: {data['port']}
    TOKEN: {data['token']}
    切记！不要告诉他人！！
    """.strip()
    await load_console_key.finish(msg)


@load_console_key.handle()
async def _(event: GroupMessageEvent):
    await load_console_key.finish("请私戳咱获取（")


del_console_key = Status().on_command("/deauth", "销毁进入网页后台的凭证", permission=SUPERUSER)


@del_console_key.got("is_sure_d", "...你确定吗(y/n)")
async def _(is_sure: str = ArgPlainText("is_sure_d")):
    if is_sure != "y":
        await del_console_key.finish("反悔了呢...")

    df = STATUS_DIR / "data.json"
    if not df.is_file():
        await del_console_key.finish("你还没向咱索取凭证呢.../auth 以获取")

    try:
        data: dict = json.loads(df.read_bytes())

        del data["data"]

        with open(df, "w", encoding="utf-8") as w:
            w.write(json.dumps(data))
    except WriteError:
        await del_console_key.send("销毁失败了...请至此处自行删除文件:\n" + str(df))
        raise WriteError("Writing / Reading file: " + str(df) + " failed!")

    await del_console_key.finish("销毁成功！如需再次获取: /auth")


res_console_key = Status().on_command("/reauth", "重置进入网页后台的凭证", permission=SUPERUSER)


@res_console_key.got("is_sure_r", "...你确定吗(y/n)")
async def _(is_sure: str = ArgPlainText("is_sure_r")):
    if is_sure != "y":
        await res_console_key.finish("反悔了呢...")

    df = STATUS_DIR / "data.json"
    if not df.is_file():
        await del_console_key.finish("你还没向咱索取凭证呢.../auth 以获取")

    try:
        data: dict = json.loads(df.read_bytes())

        del data["data"]

        with open(df, "w", encoding="utf-8") as w:
            w.write(json.dumps(data))
    except WriteError:
        await del_console_key.send("销毁失败了...请至此处自行删除文件:\n" + str(df))
        raise WriteError("Writing / Reading file: " + str(df) + " failed!")


@res_console_key.got("is_pub_r_n", "咱的运行环境是否有公网(y/n)")
async def _(event: PrivateMessageEvent, is_pub_n: str = ArgPlainText("is_pub_n")):
    if is_pub_n != "y":
        ip = str(await Status().get_host_ip(False))
        await res_console_key.send("没有公网吗...嗯知道了")
    else:
        ip = str(await Status().get_host_ip(True))

    p = BotSelfConfig.port
    rs = Status().get_random_str(20)

    df = STATUS_DIR / "data.json"
    try:
        if not df.is_file():
            with open(df, "w", encoding="utf-8") as w:
                w.write(json.dumps({}))

        d = json.loads(df.read_bytes())

        ca = d.get("data", None)
        if ca:
            await res_console_key.send("咱已经告诉你了嗷！啊！忘了.../gauth 获取吧")
            return

        d["data"] = ForAuthData(ip=ip, port=str(p), token=rs).dict()

        with open(df, "w", encoding="utf-8") as w:
            w.write(json.dumps(d))
    except WriteError:
        msg = f"""
        哦吼！写入文件失败了...还请自行记下哦...
        IP: {ip}
        PORT: {p}
        TOKEN: {rs}
        一定要保管好哦！切勿告诉他人哦！
        """.strip()
        await res_console_key.send(msg)

        raise WriteError("Writing file: " + str(df) + " failed!")

    msg = f"""
    该信息已保存！可通过 /gauth 获取~
    IP: {ip}
    PORT: {p}
    TOKEN: {rs}
    一定要保管好哦！切勿告诉他人哦！
    """.strip()
    await res_console_key.finish(msg)
