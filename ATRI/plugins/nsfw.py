import re
import json

from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.typing import T_State

from ATRI.log import logger as log
from ATRI.config import BotSelfConfig, NsfwCheck
from ATRI.service import Service as sv
from ATRI.exceptions import RequestError
from ATRI.rule import is_in_service
from ATRI.utils.request import get_bytes
from ATRI.utils.cqcode import coolq_code_check


nsfw_url = f"http://{NsfwCheck.host}:{NsfwCheck.port}/?url="


nsfw_checking = sv.on_message()


@nsfw_checking.handle()
async def _nsfw_checking(bot: Bot, event: GroupMessageEvent) -> None:
    if NsfwCheck.enabled:
        msg = str(event.message)
        user = event.user_id
        group = event.group_id
        check = await coolq_code_check(msg, user, group)

        if check:
            if "image" not in msg:
                return

            url = nsfw_url + re.findall(r"url=(.*?)]", msg)[0]
            try:
                data = json.loads(await get_bytes(url))
            except:
                log.warning("检测涩图失败，请查阅文档以获取帮助")
                return
            if round(data["score"], 4) * 100 >= NsfwCheck.passing_rate:
                score = "{:.2%}".format(round(data["score"], 4))
                log.debug(f"截获涩图，得分：{score}")
                for sup in BotSelfConfig.superusers:
                    await bot.send_private_msg(
                        user_id=sup, message=f"{msg}\n涩值: {score}"
                    )
                await bot.send(event, f"好涩哦！涩值：{score}\n不行了咱要发给主人看！")
    else:
        pass


__doc__ = """
检测你图片的涩值
权限组：所有人
用法：
  /nsfw (pic)
补充：
  pic: 图片
示例：
  /nsfw 然后Bot会向你索取图片
"""

nsfw_reading = sv.on_command(cmd="/nsfw", docs=__doc__, rule=is_in_service("nsfw"))


@nsfw_reading.args_parser  # type: ignore
async def _nsfw(bot: Bot, event: GroupMessageEvent, state: T_State) -> None:
    msg = str(event.message)
    quit_list = ["算了", "罢了", "不搜了"]
    if msg in quit_list:
        await nsfw_reading.finish("好吧")

    if not msg:
        await nsfw_reading.reject("图呢？")
    else:
        state["pic_nsfw"] = msg


@nsfw_reading.handle()
async def _nsfw_r(bot: Bot, event: GroupMessageEvent, state: T_State) -> None:
    user = event.user_id
    group = event.group_id
    msg = str(event.message).strip()
    check = await coolq_code_check(msg, user, group)
    if check and msg:
        state["pic_nsfw"] = msg


@nsfw_reading.got("pic_nsfw", prompt="图呢？")
async def _nsfw_reading(bot: Bot, event: GroupMessageEvent, state: T_State) -> None:
    msg = state["pic_nsfw"]
    pic = re.findall(r"url=(.*?)]", msg)
    if not pic:
        await nsfw_reading.reject("请发送图片而不是其它东西！！")

    url = nsfw_url + pic[0]
    try:
        data = json.loads(await get_bytes(url))
    except RequestError:
        raise RequestError("Time out!")

    score = round(data["score"], 4)
    result = "{:.2%}".format(round(data["score"], 4))
    if score >= 0.9:
        level = "hso! 我要发给主人看！"
        for sup in BotSelfConfig.superusers:
            await bot.send_private_msg(
                user_id=sup, message=f"{state['pic_nsfw']}\n涩值: {result}"
            )
    elif 0.9 > score >= 0.6:
        level = "嗯，可冲"
    else:
        level = "？能不能换张55完全冲不起来"

    repo = f"涩值：{result}\n{level}"
    await nsfw_reading.finish(repo)
