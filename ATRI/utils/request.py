import httpx

from ATRI import conf
from ATRI.log import log

timeout = conf.BotConfig.request_timeout
if timeout:
    timeout = httpx.Timeout(timeout)

if not conf.BotConfig.proxy:
    proxy = dict()
else:
    proxy = {"all://": conf.BotConfig.proxy}


async def get(url: str, **kwargs):
    log.debug(f"GET {url} by {proxy if proxy else 'No proxy'} | MORE: \n {kwargs}")
    async with httpx.AsyncClient(proxies=proxy, timeout=timeout) as client:  # type: ignore
        return await client.get(url, **kwargs)


async def post(url: str, **kwargs):
    log.debug(f"POST {url} by {proxy if proxy else 'No proxy'} | MORE: \n {kwargs}")
    async with httpx.AsyncClient(proxies=proxy, timeout=timeout) as client:  # type: ignore
        return await client.post(url, **kwargs)
