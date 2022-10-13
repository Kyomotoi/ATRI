import time
import json
from pathlib import Path
from typing import Optional
from traceback import format_exc
from pydantic.main import BaseModel

from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import ActionFailed
from nonebot.adapters.onebot.v11 import Bot, PrivateMessageEvent, GroupMessageEvent
from nonebot.message import run_postprocessor

from ATRI import conf

from .log import log
from .utils import gen_random_str


ERROR_DIR = Path(".") / "data" / "errors"
ERROR_DIR.mkdir(parents=True, exist_ok=True)


class ErrorInfo(BaseModel):
    track_id: str
    prompt: str
    time: str
    content: str


def _save_error(prompt: str, content: str) -> str:
    track_id = gen_random_str(8)
    data = ErrorInfo(
        track_id=track_id,
        prompt=prompt,
        time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        content=content,
    )
    path = ERROR_DIR / f"{track_id}.json"
    with open(path, "w", encoding="utf-8") as r:
        r.write(json.dumps(data.dict(), indent=4))
    return track_id


def load_error(track_id: str) -> dict:
    path = ERROR_DIR / f"{track_id}.json"
    return json.loads(path.read_bytes())


class BaseBotException(Exception):
    prompt: Optional[str] = "ignore"

    def __init__(self, prompt: Optional[str]) -> None:
        self.prompt = prompt or self.__class__.prompt or self.__class__.__name__
        self.track_id = _save_error(self.prompt, format_exc())
        super().__init__(self.prompt)


class NotConfigured(BaseBotException):
    prompt = "缺少配置"


class InvalidConfigured(BaseBotException):
    prompt = "无效配置"


class WriteFileError(BaseBotException):
    prompt = "写入错误"


class ReadFileError(BaseBotException):
    prompt = "读取文件失败"


class RequestError(BaseBotException):
    prompt = "网页/接口请求错误"


class GetStatusError(BaseBotException):
    prompt = "获取状态失败"


class FormatError(BaseBotException):
    prompt = "格式错误"


class ServiceRegisterError(BaseBotException):
    prompt = "服务注册错误"


class BilibiliDynamicError(BaseBotException):
    prompt = "b站动态订阅错误"


class TwitterDynamicError(BaseBotException):
    prompt = "Twitter动态订阅错误"


class ThesaurusError(BaseBotException):
    prompt = "词库相关错误"


class RssError(BaseBotException):
    prompt = "RSS订阅错误"


@run_postprocessor
async def _(bot: Bot, event, matcher: Matcher, exception: Optional[Exception]):
    if not exception:
        return

    try:
        raise exception
    except BaseBotException as err:
        prompt = err.prompt or err.__class__.__name__
        track_id = err.track_id
    except ActionFailed as err:
        prompt = "请参考协议端输出"
        track_id = _save_error(prompt, format_exc())
    except Exception as err:
        prompt = "Unknown ERROR->" + err.__class__.__name__
        track_id = _save_error(prompt, format_exc())

    if isinstance(event, PrivateMessageEvent):
        _id = "用户" + event.get_user_id()
    elif isinstance(event, GroupMessageEvent):
        _id = "群" + str(event.group_id)
    else:
        _id = "unknown"

    log.error(f"Error Track ID: {track_id}")
    msg = f"呜——出错了...追踪: {track_id}\n来自: {_id}"

    for superusers in conf.BotConfig.superusers:
        try:
            await bot.send_private_msg(user_id=superusers, message=msg)
        except BaseBotException:
            return
