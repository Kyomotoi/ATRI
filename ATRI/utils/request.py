import httpx

from ATRI.config import BotSelfConfig
from ATRI.log import logger as log

timeout = BotSelfConfig.request_timeout
if timeout:
    timeout = httpx.Timeout(timeout)

if not BotSelfConfig.proxy:
    proxy = dict()
else:
    proxy = {"all://": BotSelfConfig.proxy}


async def get(url: str, **kwargs):
    log.debug(f"GET {url} by {proxy if proxy else 'No proxy'} | MORE: \n {kwargs}")
    async with httpx.AsyncClient(proxies=proxy, timeout=timeout) as client:  # type: ignore
        return await client.get(url, **kwargs)


async def post(url: str, **kwargs):
    log.debug(f"POST {url} by {proxy if proxy else 'No proxy'} | MORE: \n {kwargs}")
    async with httpx.AsyncClient(proxies=proxy, timeout=timeout) as client:  # type: ignore
        return await client.post(url, **kwargs)
