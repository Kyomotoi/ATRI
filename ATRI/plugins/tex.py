import re
from urllib.parse import quote_plus
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State

from ATRI.exceptions import RequestTimeOut
from ATRI.rule import is_in_banlist, is_in_dormant
from ATRI.utils.request import post_bytes


ZHIHU_TEX_SVG_URL_FORMAT = 'https://www.zhihu.com/equation?tex='
LATEX2PNG_API_URL = 'http://latex2png.com/'
LATEX2PNG_IMAGE_URL_FORMAT = 'http://latex2png.com/output//'


tex = on_command("/tex", rule=is_in_banlist() & is_in_dormant())

@tex.handle()
async def _tex(bot: Bot, event: MessageEvent, state: T_State) -> None:
    tex_code = str(event.message).strip()
    if tex_code:
        state["tex_code"] = tex_code

@tex.got("tex_code", prompt="请告诉咱需要生成图片的的Tex公式")
async def __tex(bot: Bot, event: MessageEvent, state: T_State) -> None:
    tex_code = state["tex_code"]
    try:
        req = await post_bytes(
            LATEX2PNG_API_URL,
            params={
                "latex": tex_code,
                "res": "600",
                "color": "000000"
            }
        )
    except RequestTimeOut:
        raise RequestTimeOut("Failed to request!")
    
    html = str(req)
    m = re.search(r"latex_[0-9a-z]+\.png", html)
    if not m:
        await tex.finish("生成失败，等会再试试吧...")
    
    await tex.finish(
        Message(
            MessageSegment.image(LATEX2PNG_IMAGE_URL_FORMAT + m.group(0)) +
            "\n" + ZHIHU_TEX_SVG_URL_FORMAT + quote_plus(tex_code)
        )
    )
