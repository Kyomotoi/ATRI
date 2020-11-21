#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/10/11 14:43:55
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import requests
from typing import Optional
from aiohttp import ClientSession

def request_get(url: str, params: Optional[dict] = None) -> bytes:
    '''
    通过 GET 方式请求 url。

    :return: bytes
    '''
    return requests.get(url, params).content

def request_api_text(url: str) -> str:
    res = requests.request("GET", url)
    html = res.text
    return html

async def aio_get_bytes(url: str, headers: Optional[dict] = None) -> bytes:
    '''
    通过 GET 以 异步 方式请求 url。

    :return: bytes
    '''
    async with ClientSession() as asyncSession:
        async with asyncSession.get(url, headers=headers) as resp:
          result = await resp.read()
    return result