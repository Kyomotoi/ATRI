from typing import Optional
from aiohttp import ClientSession


async def get_text(url: str, headers: Optional[dict] = None) -> str:
    """异步以 Get 方式请求 url"""
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as r:
            result = await r.text()
    return result


async def get_bytes(url: str, headers: Optional[dict] = None) -> bytes:
    """异步以 Get 方式请求 url"""
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as r:
            result = await r.read()
    return result


async def post_bytes(url: str, params: Optional[dict] = None) -> bytes:
    """异步以 Post 方式请求 url"""
    async with ClientSession() as session:
        async with session.post(url, params=params) as r:
            result = await r.read()
    return result
