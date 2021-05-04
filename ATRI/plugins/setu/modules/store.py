import json
from random import choice

from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from ATRI.service import Service as sv
from ATRI.utils.request import get_bytes
from ATRI.exceptions import RequestError

from .data_source import SetuData


API_URL: str = "https://api.kyomotoi.moe/api/pixiv/illust?id="


__doc__ = """
为本地添加涩图！
权限组：维护者
用法：
  添加涩图 (pid)
补充：
  pid: Pixiv 作品id
"""


add_setu = sv.on_command(cmd="添加涩图", docs=__doc__, permission=SUPERUSER)


@add_setu.args_parser  # type: ignore
async def _load_add_setu(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    cancel = ["算了", "罢了"]
    if msg in cancel:
        await add_setu.finish("好吧...")
    if not msg:
        await add_setu.reject("涩图(pid)速发！")
    else:
        state["setu_add"] = msg


@add_setu.handle()
async def _add_setu(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["setu_add"] = msg


@add_setu.got("setu_add", prompt="涩图(pid)速发！")
async def _deal_add_setu(bot: Bot, event: MessageEvent, state: T_State) -> None:
    pid = state["setu_add"]

    URL = API_URL + pid
    try:
        data = json.loads(await get_bytes(URL))["illust"]
    except RequestError:
        raise RequestError("Request failed!")

    try:
        pic = data["meta_single_page"]["original_image_url"].replace(
            "pximg.net", "pixiv.cat"
        )
    except Exception:
        pic = choice(data["meta_pages"])["image_urls"]["original"].replace(
            "pximg.net", "pixiv.cat"
        )

    d = {
        "pid": pid,
        "title": data["title"],
        "tags": str(data["tags"]),
        "user_id": data["user"]["id"],
        "user_name": data["user"]["name"],
        "user_account": data["user"]["account"],
        "url": pic,
    }
    await SetuData.add_data(d)

    show_img = data["image_urls"]["medium"].replace("pximg.net", "pixiv.cat")
    msg = (
        "好欸！是新涩图：\n"
        f"Pid: {pid}\n"
        f"Title: {data['title']}\n"
        f"{MessageSegment.image(show_img)}"
    )
    await add_setu.finish(Message(msg))


__doc__ = """
删除涩图！
权限组：维护者
用法：
  删除涩图 (pid)
补充：
  pid: Pixiv 作品id
"""


del_setu = sv.on_command(cmd="删除涩图", docs=__doc__, permission=SUPERUSER)


@del_setu.args_parser  # type: ignore
async def _load_del_setu(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    cancel = ["算了", "罢了"]
    if msg in cancel:
        await add_setu.finish("好吧...")
    if not msg:
        await add_setu.reject("涩图(pid)速发！")
    else:
        state["setu_del"] = msg


@del_setu.handle()
async def _del_setu(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["setu_del"] = msg


@del_setu.got("setu_del", prompt="涩图(pid)速发！")
async def _deal_del_setu(bot: Bot, event: MessageEvent, state: T_State) -> None:
    pid = int(state["setu_del"])
    await SetuData.del_data(pid)
    await del_setu.finish(f"涩图({pid})已删除...")


count_setu = sv.on_command(cmd="涩图总量", permission=SUPERUSER)


@count_setu.handle()
async def _count_setu(bot: Bot, event: MessageEvent) -> None:
    msg = f"咱本地搭载了 {await SetuData.count()} 张涩图！"
    await count_setu.finish(msg)
