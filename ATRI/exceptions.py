import time
import json
import string
from pathlib import Path
from random import sample
from typing import Optional
from traceback import format_exc
from pydantic.main import BaseModel

from nonebot.adapters.cqhttp import MessageEvent
from nonebot.matcher import Matcher
from nonebot.message import run_postprocessor

from .log import logger


ERROR_FILE = Path('.') / 'ATRI' / 'data' / 'errors'
ERROR_FILE.parent.mkdir(exist_ok=True, parents=True)


class ExceptionInfo(BaseModel):
    error_id: str
    prompt: str
    time: str
    error_content: str


def store_error(error_id: str, prompt, error_content: str) -> None:
    data = ExceptionInfo(
        error_id=error_id,
        prompt=prompt,
        time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        error_content=error_content
    )

    path = ERROR_FILE / f"{error_id}.json"
    path.parent.mkdir(exist_ok=True, parents=True)
    with open(path, 'w', encoding='utf-8') as target:
        target.write(
            json.dumps(
                data.dict(), indent=4
            )
        )


def read_error(error_id: str) -> dict:
    path = ERROR_FILE / f"{error_id}.json"
    try:
        with open(path, 'r', encoding='utf-8') as target:
            data = target.read()
        return json.loads(data)
    except FileNotFoundError:
        raise FileNotFoundError


class BaseBotException(BaseException):
    prompt: Optional[str] = 'ignore'

    def __init__(self, prompt: Optional[str]) -> None:
        super().__init__(self)
        self.prompt = prompt or self.__class__.prompt \
            or self.__class__.__name__
        self.error_content = format_exc()
        self.error_id = ''.join(
            sample(string.ascii_letters + string.digits, 16)
        )


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


@run_postprocessor  # type: ignore
async def _(matcher: Matcher, exception: Optional[Exception],
            event: MessageEvent, state: dict) -> None:
    """检测Bot运行中的报错，并进行提醒"""
    print(114514)
    if not exception:
        return
    
    try:
        raise exception
    except BaseBotException as Error:
        prompt = Error.prompt or Error.__class__.__name__
        error_id = Error.error_id
        # error_content = format_exc()
    except Exception as Error:
        prompt = "Unknown ERROR" + Error.__class__.__name__
        error_id = ''.join(
            sample(string.ascii_letters + string.digits, 16)
        )
        store_error(error_id, prompt, format_exc())

    logger.debug(f"A bug has been cumming, trace ID: {error_id}")
    msg = (
        "[WARNING] 这是一个错误...\n"
        f"Track ID: {error_id}\n"
        f"Reason: {prompt}\n"
        "ごんめなさい... ;w;"
    )
    
    await matcher.finish(msg)
