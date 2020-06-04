import json
import asyncio
import requests
from typing import Any
from functools import partial
from nonebot import on_command, CommandSession


class AsyncResponse:
    def __init__(self, response: requests.Response):
        self.raw_response = response

async def run_sync_func(func, *args, **kwargs) -> Any:
    return await asyncio.get_event_loop().run_in_executor(
        None, partial(func, *args, **kwargs))

async def request(method, url, **kwargs) -> AsyncResponse:
    return AsyncResponse(await run_sync_func(requests.request,
                                             method=method, url=url, **kwargs))


url = "https://api.imjad.cn/hitokoto/?cat=a&charset=utf-8&length=50&encode=&fun=sync&source="


@on_command('hitokoto', aliases=['一言'], only_to_me=False)
async def _(session: CommandSession):
    res = requests.get(url)
    if not res.ok:
        session.finish('获取失败')
    session.finish(res.text)