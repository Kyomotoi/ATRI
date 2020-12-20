from typing import Optional
from aiohttp.client import ClientSession


class Request():
    async def get(self, url: str, headers: Optional[dict] = None) -> bytes:
        async with ClientSession() as session:
            async with session.get(url, headers=headers) as r:
                result = await r.read()
        return result
