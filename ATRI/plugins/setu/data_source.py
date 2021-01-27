import json
from pathlib import Path

from ATRI.config import SETU_CONFIG
from ATRI.request import Request
from ATRI.exceptions import InvalidRequest


DATA_PATH = Path('.') / 'ATRI' / 'data' / 'database'

async def setu_port() -> dict:
    url = SETU_CONFIG['setu']['link']['url']
    params = {
        "apikey": SETU_CONFIG['setu']['link']['api_key'],
        "r18": 0,
        "num": 1
    }
    data = {}
    try:
        data = json.loads(await Request.post_bytes(url, params))
    except InvalidRequest:
        raise InvalidRequest('Request failed!')
    return data


async def setu_local() -> str:
    ...
