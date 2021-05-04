from typing import Optional
from aiohttp import ClientSession


async def get_text(url: str, headers: Optional[dict] = None) -> str:
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as r:
            result = await r.text()
    return result


async def get_bytes(url: str, headers: Optional[dict] = None) -> bytes:
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as r:
            result = await r.read()
    return result


async def get_content(url: str, headers: Optional[dict] = None):
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as r:
            result = await r.content.read()
    return result


async def post_bytes(
    url: str, params: Optional[dict] = None, json: Optional[dict] = None
) -> bytes:
    async with ClientSession() as session:
        async with session.post(url, params=params, json=json) as r:
            result = await r.read()
    return result
