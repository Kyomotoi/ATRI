import httpx
from ATRI.config import BotSelfConfig


if not BotSelfConfig.proxy:
    proxy = dict()
else:
    proxy = {"all://": BotSelfConfig.proxy}


async def get(url: str, **kwargs):
    async with httpx.AsyncClient(proxies=proxy) as client:  # type: ignore
        return await client.get(url, **kwargs)


async def post(url: str, **kwargs):
    async with httpx.AsyncClient(proxies=proxy) as client:  # type: ignore
        return await client.post(url, **kwargs)
