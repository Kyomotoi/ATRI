import re
import json
from random import choice, random

from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.adapters.cqhttp.message import Message

from ATRI.service import Service as sv
from ATRI.rule import is_in_service
from ATRI.utils.request import get_bytes, post_bytes
from ATRI.utils.limit import is_too_exciting
from ATRI.config import Setu, BotSelfConfig
from ATRI.exceptions import RequestError

from .data_source import Hso, SIZE_REDUCE, SetuData


LOLICON_URL: str = "https://api.lolicon.app/setu/"
PIXIV_URL: str = (
    "https://api.kyomotoi.moe/api/pixiv/search?mode=exact_match_for_tags&word="
)
R18_ENABLED: int = 0
USE_LOCAL_DATA: bool = False
MIX_LOCAL_DATA: bool = False


setu = sv.on_regex(
    r"来[张点][色涩]图|[涩色]图来|想要[涩色]图|[涩色]图[Tt][Ii][Mm][Ee]", rule=is_in_service("setu")
)


@setu.handle()
async def _setu(bot: Bot, event: MessageEvent) -> None:
    user = event.user_id
    check = is_too_exciting(user, 3, hours=1)
    if not check:
        return

    await bot.send(event, "别急，在找了！")
    params = {"apikey": Setu.key, "r18": str(R18_ENABLED), "size1200": "true"}
    try:
        data = json.loads(await post_bytes(LOLICON_URL, params))["data"][0]
    except RequestError:
        raise RequestError("Request failed!")

    check = await Hso.nsfw_check(data["url"])
    score = "{:.2%}".format(check, 4)

    if not MIX_LOCAL_DATA:
        if USE_LOCAL_DATA:
            data = choice(await SetuData.get_setu())  # type: ignore
            data = {"pid": data[0], "title": data[1], "url": data[6]}
            if random() <= 0.1:
                await bot.send(event, "我找到图了，但我发给主人了❤")
                msg = await Hso.setu(data) + f"\n由用户({user})提供"
                for sup in BotSelfConfig.superusers:
                    await bot.send_private_msg(user_id=sup, message=msg)
            else:
                await setu.finish(Message(await Hso.setu(data)))
        else:
            if check >= 0.9:
                if random() <= 0.2:
                    repo = "我找到图了，但我发给主人了❤\n" f"涩值：{score}"
                    await bot.send(event, repo)
                    msg = await Hso.setu(data) + f"\n由用户({user})提供，涩值：{score}"
                    for sup in BotSelfConfig.superusers:
                        await bot.send_private_msg(user_id=sup, message=msg)
                else:
                    await setu.finish(Message(await Hso.setu(data)))
            else:
                if random() <= 0.1:
                    await bot.send(event, "我找到图了，但我发给主人了❤")
                    msg = await Hso.setu(data) + f"\n由用户({user})提供，涩值：{score}"
                    for sup in BotSelfConfig.superusers:
                        await bot.send_private_msg(user_id=sup, message=msg)
                else:
                    await setu.finish(Message(await Hso.setu(data)))
    else:
        if random() <= 0.5:
            if random() <= 0.1:
                await bot.send(event, "我找到图了，但我发给主人了❤")
                msg = await Hso.setu(data) + f"\n由用户({user})提供"
                for sup in BotSelfConfig.superusers:
                    await bot.send_private_msg(user_id=sup, message=msg)
            else:
                await setu.finish(Message(await Hso.setu(data)))
        else:
            data = choice(await SetuData.get_setu())  # type: ignore
            data = {"pid": data[0], "title": data[1], "url": data[6]}
            if random() <= 0.1:
                await bot.send(event, "我找到图了，但我发给主人了❤")
                msg = await Hso.setu(data) + f"\n由用户({user})提供"
                for sup in BotSelfConfig.superusers:
                    await bot.send_private_msg(user_id=sup, message=msg)
            else:
                await setu.finish(Message(await Hso.setu(data)))


key_setu = sv.on_regex(r"来[点张](.*?)的[涩色🐍]图", rule=is_in_service("setu"))


@key_setu.handle()
async def _key_setu(bot: Bot, event: MessageEvent) -> None:
    user = event.user_id
    check = is_too_exciting(user, 10, hours=1)
    if not check:
        await setu.finish("休息一下吧❤")

    await bot.send(event, "别急，在找了！")
    msg = str(event.message).strip()
    tag = re.findall(r"来[点张](.*?)的?[涩色🐍]图", msg)[0]
    URL = PIXIV_URL + tag

    try:
        data = json.loads(await get_bytes(URL))["illusts"]
    except RequestError:
        raise RequestError("Request msg failed!")

    if random() <= 0.1:
        await bot.send(event, "我找到图了，但我发给主人了❤")
        msg = await Hso.acc_setu(data) + f"\n由用户({user})提供"
        for sup in BotSelfConfig.superusers:
            await bot.send_private_msg(user_id=sup, message=msg)
    else:
        await setu.finish(Message(await Hso.acc_setu(data)))


__doc__ = """
涩图设置
权限组：维护者
用法：
  涩图设置 启用/禁用r18
  涩图设置 启用/禁用压缩
  涩图设置 启用/禁用本地涩图
  涩图设置 启用/禁用混合本地涩图
"""

setu_config = sv.on_command(cmd="涩图设置", docs=__doc__, permission=SUPERUSER)


@setu_config.handle()
async def _setu_config(bot: Bot, event: MessageEvent) -> None:
    global R18_ENABLED, SIZE_REDUCE, USE_LOCAL_DATA, MIX_LOCAL_DATA
    msg = str(event.message).split(" ")
    if msg[0] == "":
        repo = "可用设置如下：\n启用/禁用r18\n启用/禁用压缩\n启用/禁用本地涩图\n启用/禁用混合本地涩图"
        await setu_config.finish(repo)
    elif msg[0] == "启用r18":
        R18_ENABLED = 1
        await setu_config.finish("已启用r18")
    elif msg[0] == "禁用r18":
        R18_ENABLED = 0
        await setu_config.finish("已禁用r18")
    elif msg[0] == "启用压缩":
        SIZE_REDUCE = True
        await setu_config.finish("已启用图片压缩")
    elif msg[0] == "禁用压缩":
        SIZE_REDUCE = False
        await setu_config.finish("已禁用图片压缩")
    elif msg[0] == "启用本地涩图":
        USE_LOCAL_DATA = True
        await setu_config.finish("已启用本地涩图")
    elif msg[0] == "禁用本地涩图":
        USE_LOCAL_DATA = False
        await setu_config.finish("已禁用本地涩图")
    elif msg[0] == "启用混合本地涩图":
        MIX_LOCAL_DATA = True
        await setu_config.finish("已启用混合本地涩图")
    elif msg[0] == "禁用混合本地涩图":
        MIX_LOCAL_DATA = False
        await setu_config.finish("已禁用混合本地涩图")
    else:
        await setu_config.finish("阿！请检查拼写")


not_get_se = sv.on_command("不够涩")


@not_get_se.handle()
async def _not_se(bot: Bot, event: MessageEvent) -> None:
    user = event.user_id
    check = is_too_exciting(user, 1, 120)
    if check:
        msg = choice(["那你来发", "那你来发❤"])
        await not_get_se.finish(msg)
