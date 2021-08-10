from typing import Optional
from aiohttp import ClientSession, ClientResponse, FormData


class Response:
    def __init__(self, response: ClientResponse) -> None:
        self.raw_response = response

    @property
    def status(self) -> int:
        return self.raw_response.status

    @property
    def url(self):
        return self.raw_response.url

    @property
    def real_url(self):
        return self.raw_response.real_url

    @property
    def host(self):
        return self.raw_response.host

    @property
    def headers(self):
        return self.raw_response.headers

    @property
    def raw_headers(self):
        return self.raw_response.raw_headers

    @property
    def request_info(self):
        return self.raw_response.request_info

    @property
    async def read(self):
        return await self.raw_response.read()

    @property
    async def text(self):
        return await self.raw_response.text()

    async def json(self):
        return await self.raw_response.json()


async def get(url, params: dict = None, **kwargs) -> Response:
    return Response(await ClientSession().get(url=url, params=params, **kwargs))


async def post(url, data: Optional[FormData] = None, **kwargs) -> Response:
    return Response(await ClientSession().post(url=url, data=data, **kwargs))
