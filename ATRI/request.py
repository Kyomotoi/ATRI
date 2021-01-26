import os
import string
import aiofiles
from random import sample
from pathlib import Path
from typing import Optional
from aiohttp.client import ClientSession

from .exceptions import InvalidWriteText


TEMP_PATH = Path('.') / 'ATRI' / 'data' / 'temp'
os.makedirs(TEMP_PATH, exist_ok=True)


class Request:
    @staticmethod
    async def get_text(url: str, headers: Optional[dict] = None) -> str:
        '''
        异步方式请求接口
        :return: text
        '''
        async with ClientSession() as session:
            async with session.get(url, headers=headers) as r:
                result = await r.text()
        return result

    @staticmethod
    async def get_bytes(url: str, headers: Optional[dict] = None) -> bytes:
        '''
        异步方式请求接口
        :return: bytes
        '''
        async with ClientSession() as session:
            async with session.get(url, headers=headers) as r:
                result = await r.read()
        return result

    @classmethod
    async def get_image(cls, url: str) -> Path:
        '''
        异步方式下载图片
        :return: img file
        '''
        file_path = TEMP_PATH / 'img'
        file_name = ''.join(sample(string.ascii_letters + string.digits, 16))
        img_path = file_path / f'{file_name}.png'
        image = await cls.get_bytes(url)
        try:
            async with aiofiles.open(image, 'wb') as f:
                await f.write(image)
        except InvalidWriteText:
            raise InvalidWriteText('Writing file failed!')
        return img_path

    @staticmethod
    async def post_bytes(url: str, params: Optional[dict] = None) -> bytes:
        '''
        异步方式 Post 接口
        :return: bytes
        '''
        async with ClientSession() as session:
            async with session.post(url, params=params) as r:
                result = await r.read()
        return result