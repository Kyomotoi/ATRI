import os
import time
import json
import string
from pathlib import Path
from random import sample
from typing import Optional
from traceback import format_exc

from nonebot.adapters.cqhttp import Bot, Event
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nonebot.message import run_postprocessor

from .log import logger


ERROR_DIR = Path('.') / 'ATRI' / 'data' / 'errors'
os.makedirs(ERROR_DIR, exist_ok=True)


def _save_error(prompt: str, content: str) -> str:
    track_id = ''.join(sample(string.ascii_letters + string.digits, 16))
    data = {
        "track_id": track_id,
        "prompt": prompt,
        "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "content": content
    }
    path = ERROR_DIR / f'{track_id}.json'
    with open(path, 'w', encoding='utf-8') as r:
        r.write(json.dumps(data, indent=4))
    return track_id


def load_error(track_id: str) -> dict:
    path = ERROR_DIR / f'{track_id}.json'
    return json.loads(path.read_bytes())


class BaseBotException(BaseException):
    prompt: Optional[str] = 'ignore'

    def __init__(self, prompt: Optional[str]) -> None:
        self.prompt = prompt or self.__class__.prompt \
            or self.__class__.__name__
        self.track_id = _save_error(self.prompt, format_exc())
        super().__init__(self.prompt)


class NotConfigured(BaseBotException):
    prompt = "缺少配置"


class InvalidConfigured(BaseBotException):
    prompt = "无效配置"


class WriteError(BaseBotException):
    prompt = "写入错误"


class LoadingError(BaseBotException):
    prompt = "加载错误"


class RequestTimeOut(BaseBotException):
    prompt = "网页/接口请求超时"


class GetStatusError(BaseBotException):
    prompt = "获取状态失败"


@run_postprocessor  # type: ignore
async def _track_error(matcher: Matcher,
                       exception: Optional[Exception],
                       bot: Bot,
                       event: Event,
                       state: T_State) -> None:
    if exception is None:
        return
    
    try:
        raise exception
    except BaseBotException as Error:
        prompt = Error.prompt or Error.__class__.__name__
        track_id = Error.track_id
    except Exception as Error:
        prompt = "Unknown ERROR->" + Error.__class__.__name__
        track_id = _save_error(prompt, format_exc())

    logger.debug(f"A bug has been cumming, trace ID: {track_id}")
    msg = (
        "[WARNING] 这是一个错误... ;w;\n"
        f"追踪ID: {track_id}\n"
        f"触发原因: {prompt}\n"
        "键入 /来杯红茶 以联系维护者"
    )
    
    await bot.send(event, msg)
