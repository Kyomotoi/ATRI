# -*- coding:utf-8 -*-
import requests
from aiohttp import ClientSession

def request_api(url):
    response = requests.request("GET", url)
    html = response.text
    return html

def request_api_params(url, params):
    response = requests.get(url, params = params)
    html = response.text
    return html

async def post_bytes(url, headers=None,data=None):
    async with ClientSession() as asyncsession:
        async with asyncsession.post(url,headers=headers,data=data) as response:
            b = await response.read()
    return b