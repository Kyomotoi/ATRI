import os
import json
import string
import time
from pydantic import BaseModel
from typing import Optional
import aiofiles
from random import sample
from pathlib import Path
from traceback import format_exc

from nonebot.matcher import Matcher
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.message import run_postprocessor
from nonebot.adapters.cqhttp.message import MessageSegment

from .service.send import Send
from .log import logger


class Error:
    ERROR_FILE = Path('.') / 'ATRI' / 'data' / 'error'
    ERROR_FILE.parent.mkdir(exist_ok=True, parents=True)
        
    class ExceptionInfo(BaseModel):
        time: str
        rais: str
        stack: str

    @classmethod
    def _get_file(cls, error_id: str) -> Path:
        file_name = error_id + '.json'
        path = cls.ERROR_FILE / file_name
        path.parent.mkdir(exist_ok=True, parents=True)
        return path

    @classmethod
    async def capture_error(cls,
                            rais: Optional[str],
                            error_id: str) -> str:
        data = cls.ExceptionInfo(
            time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            rais=rais,
            stack=format_exc()
        )
        async with aiofiles.open(cls.ERROR_FILE, 'w',
                                 encoding='utf-8') as target:
            await target.write(
                json.dumps(data.dict(), indent=4))
        logger.debug(
            f'An error occurred！Writing file success!，track id：{error_id}')
        return error_id

    @classmethod
    async def store_error(cls, rais: str, exc):
        error_id = ''.join(sample(string.ascii_letters + string.digits, 16))
        data = cls.ExceptionInfo(
            time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            rais=rais,
            stack=exc
        )
        async with aiofiles.open(cls._get_file(error_id), 'w',
                                 encoding='utf-8') as target:
            await target.write(
                json.dumps(data.dict(), indent=4))
        logger.debug(
            f'An error occurred！Writing file success!，track id：{error_id}')
        return error_id

    @classmethod
    async def read_error(cls, error_id: str):
        path = cls._get_file(error_id)
        async with aiofiles.open(path, 'r', encoding='utf-8') as target:
            data = await target.read()
        return cls.ExceptionInfo(**json.loads(data))


class ATRIError(BaseException):
    msg: Optional[str] = None

    async def __init__(self, msg: Optional[str]) -> None:
        super().__init__(self)
        self.msg = msg or self.__class__.msg or self.__class__.__name__
        self.error = format_exc()
        self.error_id = ''.join(
            sample(string.ascii_letters + string.digits, 16))
        await Error.capture_error(rais=self.msg, error_id=self.error_id)


class BotSelfError(ATRIError):
    msg = '程序自身错误'


class InvalidConfig(ATRIError):
    msg = '配置文件有问题'


class InvalidRequest(ATRIError):
    msg = '网络请求错误'


class InvalidWriteText(ATRIError):
    msg = '写入目标失败'


class InvalidSetting(ATRIError):
    msg = '改变变量失败'


class InvalidLoad(ATRIError):
    msg = '读取失败'


@run_postprocessor # type: ignore
async def _(matcher: Matcher, exception: Optional[Exception], bot: Bot,
            event: MessageEvent, state: dict) -> None:
    if not exception:
        return

    error_id = ''
    try:
        raise exception
    except ATRIError as error:
        error_msg = error.msg
        error_id = error.error_id
        # exc = error
    except Exception as error:
        error_msg = 'Unknown ERROR' + error.__class__.__name__
        try:
            error_id = await Error.store_error(rais=str(error), exc=format_exc())
        except:
            await matcher.finish(
                MessageSegment.image(
                    file=f"file:///{Path('.').resolve() / 'ATRI' / 'data' / 'emoji' / 'error.jpg'}"))
            repo_msg = (
                "发生了意料之外的错误///\n"
                "报错连自己都无法截取惹...\n"
                "请翻阅log吧...顺便发个issues（\n"
                f"Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
            )
            await Send.send_to_superuser(repo_msg)

    logger.debug(
        f'An error occurred！Writing file success!，track id：{error_id}')
    await bot.send(
        event,
        message=MessageSegment.image(
            file=f"file:///{Path('.').resolve() / 'ATRI' / 'data' / 'emoji' / 'error.jpg'}")
    )
    repo_msg = (
        "WARNING, This is an ERROR!\n"
        f"Track ID: {error_id}\n"
        f"Reason: {error_msg}\n"
        f"Please contact author!"
    )
    await Send.send_to_superuser(repo_msg)
