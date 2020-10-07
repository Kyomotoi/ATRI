#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from typing import Optional
from aiohttp import ClientSession

def request_get(url: str, params: Optional[dict] = None) -> bytes:
    """
    :说明:

      通过 GET 方式请求 url。
    
    :参数:

      * ``url: str``: 目标网址
      * ``params: Optional[dict] = None``: 参数，若不传入则为空
    
    :返回:

      requests.content
    
    :用法:

    .. code-block:: python

        request_get(url="www.demo.com", params=params)
    
    """
    return requests.get(url, params).content

async def aio_get_bytes(url: str, headers: Optional[dict] = None):
    """
      :说明:

        通过 GET 以 异步 方式请求 url。
      
      :参数:

        * ``url: str``: 目标网址
        * ``headers: Optional[dict] = None``: 参数，若不传入则为空
      
      :返回:

        bytes
      
      :用法:

      .. code-block:: python

          aio_get_bytes(url="www.demo.com", headers=headers)
      
      """
    async with ClientSession() as asyncSession:
        async with asyncSession.get(url, headers=headers) as resp:
          result = await resp.read()
    return result