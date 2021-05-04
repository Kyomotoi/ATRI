from aiohttp import FormData

from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.service import Service as sv
from ATRI.log import LOGGER_DIR, NOW_TIME
from ATRI.utils.file import open_file
from ATRI.utils.ub_paste import paste
from ATRI.exceptions import load_error


level_list = ["info", "warning", "error", "debug"]


__doc__ = """
获取控制台信息
权限组：维护者
用法：
  获取log 等级 行数
示例：
  获取log info -20（最新20行）
"""

get_console = sv.on_command(
    cmd="获取log",
    aliases={"获取LOG", "获取控制台", "获取控制台信息"},
    docs=__doc__,
    permission=SUPERUSER,
)


@get_console.handle()
async def _get_console(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).split(" ")
    if msg:
        state["level"] = msg[0]
        try:
            state["line"] = msg[1]
        except Exception:
            pass


@get_console.got("level", prompt="需要获取的等级是？")
async def _got(bot: Bot, event: MessageEvent, state: T_State) -> None:
    quit_list = ["算了", "罢了", "不了"]
    if state["level"] in quit_list:
        await get_console.finish("好吧...")


@get_console.got("line", prompt="需要获取的行数是？")
async def _deal_get(bot: Bot, event: MessageEvent, state: T_State) -> None:
    level = state["level"]
    line = state["line"]
    repo = str()

    path = LOGGER_DIR / f"{level}" / f"{NOW_TIME}.log"
    logs = await open_file(path, "readlines")

    try:
        content = logs[int(line) :]  # type: ignore
        repo = "\n".join(content).replace("[36mATRI[0m", "ATRI")
    except IndexError:
        await get_console.finish(f"行数错误...max: {len(logs)}")  # type: ignore

    data = FormData()
    data.add_field("poster", "ATRI running log")
    data.add_field("syntax", "text")
    data.add_field("expiration", "day")
    data.add_field("content", repo)

    msg0 = f"> {event.sender.nickname}\n"
    msg0 = msg0 + f"详细请移步此处~\n{await paste(data)}"
    await track_error.finish(msg0)


__doc__ = """
追踪错误
权限组：维护者
用法：
  track 追踪ID
"""

track_error = sv.on_command(
    cmd="track", aliases={"追踪"}, docs=__doc__, permission=SUPERUSER
)


@track_error.args_parser  # type: ignore
async def _track_error_load(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    cancel = ["算了", "罢了"]
    if msg in cancel:
        await track_error.finish("好吧...")
    if not msg:
        await track_error.reject("欸？！要开始debug了吗，请提供追踪ID...Ծ‸Ծ")
    else:
        state["track"] = msg


@track_error.handle()
async def _track_error(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["track"] = msg


@track_error.got("track", prompt="欸？！要开始debug了吗，请提供追踪ID...Ծ‸Ծ")
async def _deal_track(bot: Bot, event: MessageEvent, state: T_State) -> None:
    track_id = state["track"]
    data = dict()

    try:
        data = load_error(track_id)
    except BaseException:
        await track_error.finish("未发现对应ID呢...(⇀‸↼‶)")

    msg = (
        f"ID: [{track_id}]\n"
        f"Time: [{data['time']}]\n"
        f"Prompt: [{data['prompt']}]\n"
        "——————\n"
        f"{data['content']}"
    )

    data = FormData()
    data.add_field("poster", track_id)
    data.add_field("syntax", "text")
    data.add_field("expiration", "day")
    data.add_field("content", msg)

    msg0 = f"> {event.sender.nickname}\n"
    msg0 = msg0 + f"详细请移步此处~\n{await paste(data)}"
    await track_error.finish(msg0)
