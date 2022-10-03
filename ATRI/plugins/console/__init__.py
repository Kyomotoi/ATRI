import json

from nonebot.params import ArgPlainText
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent

from ATRI.config import BotSelfConfig
from ATRI.exceptions import WriteFileError

from .data_source import Console, CONSOLE_DIR
from .models import AuthData


gen_console_key = Console().cmd_as_group("auth", "获取进入网页后台的凭证")


@gen_console_key.got("is_pub_n", "咱的运行环境是否有公网(y/n)")
async def _(event: PrivateMessageEvent, is_pub_n: str = ArgPlainText("is_pub_n")):
    data_path = CONSOLE_DIR / "data.json"
    if not data_path.is_file():
        with open(data_path, "w", encoding="utf-8") as w:
            w.write(json.dumps(dict()))

    if is_pub_n != "y":
        host = str(await Console().get_host_ip(False))
        await gen_console_key.send("没有公网吗...嗯知道了")
    else:
        host = str(await Console().get_host_ip(True))

    port = BotSelfConfig.port
    token = Console().get_random_str(20)

    data = json.loads(data_path.read_bytes())
    data["data"] = AuthData(token=token).dict()
    with open(data_path, "w", encoding="utf-8") as w:
        w.write(json.dumps(data))

    msg = f"""控制台信息已生成！
    请访问: {host}:{port}
    Token: {token}
    该 token 有效时间为 15min
    """.strip()
    await gen_console_key.finish(msg)


@gen_console_key.handle()
async def _(event: GroupMessageEvent):
    await gen_console_key.finish("请私戳咱获取（")


del_console_key = Console().cmd_as_group("del", "销毁进入网页后台的凭证")


@del_console_key.got("is_sure_d", "...你确定吗(y/n)")
async def _(is_sure: str = ArgPlainText("is_sure_d")):
    if is_sure != "y":
        await del_console_key.finish("反悔了呢...")

    df = CONSOLE_DIR / "data.json"
    if not df.is_file():
        await del_console_key.finish("你还没向咱索取凭证呢.../con.auth 以获取")

    try:
        data: dict = json.loads(df.read_bytes())

        del data["data"]

        with open(df, "w", encoding="utf-8") as w:
            w.write(json.dumps(data))
    except Exception:
        await del_console_key.send("销毁失败了...请至此处自行删除文件:\n" + str(df))
        raise WriteFileError("Writing / Reading file: " + str(df) + " failed!")

    await del_console_key.finish("销毁成功！如需再次获取: /con.auth")


from ATRI import driver as dr
from .data_source import init_resource
from .driver import init_driver


dr().on_startup(init_resource)
dr().on_startup(init_driver)
