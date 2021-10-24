import httpx
from ATRI.config import BotSelfConfig


proxy = BotSelfConfig.proxy
if not proxy:
    proxy = dict()


async def get(url: str, **kwargs):
    async with httpx.AsyncClient(proxies=proxy) as client:
        return await client.get(url, **kwargs)


async def post(url: str, **kwargs):
    async with httpx.AsyncClient(proxies=proxy) as client:
        return await client.post(url, **kwargs)
