#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   app.py
@Time    :   2020/10/24 00:25:34
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import json
import time
import sqlite3
import uvicorn
from enum import Enum
from pathlib import Path
from fastapi import FastAPI
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from utils.utils_yml import load_yaml
from utils.utils_request import aio_get_bytes

# 急着去上学写乱了下次一定改别骂了别骂了我爪巴爪巴爪巴
# orz orz orz orz orz

app = FastAPI()
tmp_API = Jinja2Templates(directory='ATRI/data/data_HTML/api')
tmp_HELP = Jinja2Templates(directory='ATRI/data/data_HTML/user')


async def get_ip_info(ip: str) -> None:
    URL = await aio_get_bytes(
        f"http://ip-api.com/json/{ip}?lang=zh-CN&fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
    )
    info = json.loads(URL)
    return info


def check_visitors(query: str):
    try:
        with open(
                Path('.') / 'ATRI' / 'data' / 'data_HTML' / 'api' / 'data' /
                'banip' / 'banip.json', 'r') as f:
            data = json.load(f)
    except:
        data = {}

    if query in data:
        return False
    else:
        return True


async def load_setu(name: str):
    file_type = 'normal'
    s_type = 'normal'

    if name == "normal":
        file_type = file_setu_normal
        s_type = "normal"

    elif name == "nearR18":
        file_type = file_setu_nearR18
        s_type = "nearR18"

    elif name == "R18":
        file_type = file_setu_R18
        s_type = "r18"

    else:
        return {"code": 404, "data": "", "msg": "Can't find aims type!"}

    con = sqlite3.connect(file_type)
    cur = con.cursor()
    info = cur.execute(f'SELECT * FROM {s_type} ORDER BY RANDOM() limit 1;')
    for i in info:
        pid = i[0]
        title = i[1]
        tags = i[2]
        account = i[3]
        name = i[4]
        u_id = i[5]
        user_link = i[6]
        img = i[7]
        print('success!')
        con.commit()
        con.close()
        return {
            "code": 200,
            "pid": pid,
            "title": title,
            "tags": tags,
            "account": account,
            "name": name,
            "u_id": u_id,
            "user_link": user_link,
            "img": img
        }


file_setu_normal = Path(
    '.') / 'ATRI' / 'data' / 'data_Sqlite' / 'setu' / 'normal.db'
file_setu_nearR18 = Path(
    '.') / 'ATRI' / 'data' / 'data_Sqlite' / 'setu' / 'nearR18.db'
file_setu_R18 = Path('.') / 'ATRI' / 'data' / 'data_Sqlite' / 'setu' / 'r18.db'

con = sqlite3.connect(file_setu_normal)  # setu-normal
cur = con.cursor()
cur.execute("select * from normal")
data_normal = len(cur.fetchall())
con.close()

con = sqlite3.connect(file_setu_nearR18)  # setu-nearR18
cur = con.cursor()
cur.execute("select * from nearR18")
data_nearR18 = len(cur.fetchall())
con.close()

con = sqlite3.connect(file_setu_R18)  # setu-r18
cur = con.cursor()
cur.execute("select * from r18")
data_r18 = len(cur.fetchall())
con.close()


class SetuModelName(str, Enum):
    noraml = "normal"
    nearR18 = "nearR18"
    R18 = "r18"


localtime = time.asctime(time.localtime(time.time()))


@app.get("/api")
async def index(request: Request):
    ip = request.client.host
    port = request.client.port
    query = str(ip) + ":" + str(port)
    info = await get_ip_info(ip)

    try:
        with open(
                Path('.') / 'ATRI' / 'data' / 'data_HTML' / 'api' / 'data' /
                'times' / 'api_all.json', 'r') as f:
            data_all = json.load(f)
    except:
        data_all = {}

    try:
        with open(
                Path('.') / 'ATRI' / 'data' / 'data_HTML' / 'api' / 'data' /
                'times' / 'api_index.json', 'r') as f:
            data_index = json.load(f)
    except:
        data_index = {}

    info = await get_ip_info(ip)
    data_all[f"{time.time()}"] = [query, info, "index"]
    data_index[f"{time.time()}"] = [query, info]

    with open(
            Path('.') / 'ATRI' / 'data' / 'data_HTML' / 'api' / 'data' /
            'times' / 'api_all.json', 'w') as f:
        f.write(json.dumps(data_all))
        f.close()

    with open(
            Path('.') / 'ATRI' / 'data' / 'data_HTML' / 'api' / 'data' /
            'times' / 'api_index.json', 'w') as f:
        f.write(json.dumps(data_index))
        f.close()

    return tmp_API.TemplateResponse(
        'index.html', {
            'request': request,
            'data_normal': data_normal,
            'data_nearR18': data_nearR18,
            'data_r18': data_r18,
            'times_all': 4,
            'date_now': localtime,
            'times_now': 6,
            'date_yesterday': 7,
            'times_yesterday': 8,
            'date_before_yesterday': 9,
            'times_before_yesterday': 10,
            'info_ip': query,
            'info_continent': info["continent"],
            'info_country': info["country"],
            'info_regionName': info["regionName"],
            'info_city': info["city"],
            'info_lat': info["lat"],
            'info_lon': info["lon"],
            'info_timezone': info["timezone"],
            'info_isp': info["isp"],
            'info_as': info["as"],
            'info_asname': info["asname"]
        })


@app.get("/api/setu/{s_type}")
async def get_setu(s_type: str, request: Request):
    ip = request.client.host
    port = request.client.port
    query = str(ip) + ":" + str(port)

    try:
        with open(
                Path('.') / 'ATRI' / 'data' / 'data_HTML' / 'api' / 'data' /
                'times' / 'api_all.json', 'r') as f:
            data_all = json.load(f)
    except:
        data_all = {}

    try:
        with open(
                Path('.') / 'ATRI' / 'data' / 'data_HTML' / 'api' / 'data' /
                'times' / 'api_setu.json', 'r') as f:
            data_setu = json.load(f)
    except:
        data_setu = {}

    info = await get_ip_info(ip)
    data_all[f"{time.time()}"] = [query, info, "setu"]
    data_setu[f"{time.time()}"] = [query, info]

    with open(
            Path('.') / 'ATRI' / 'data' / 'data_HTML' / 'api' / 'data' /
            'times' / 'api_all.json', 'w') as f:
        f.write(json.dumps(data_all))
        f.close()

    with open(
            Path('.') / 'ATRI' / 'data' / 'data_HTML' / 'api' / 'data' /
            'times' / 'api_setu.json', 'w') as f:
        f.write(json.dumps(data_setu))
        f.close()

    if check_visitors(query):
        if s_type == SetuModelName.noraml:
            return await load_setu(s_type)

        elif s_type == SetuModelName.nearR18:
            return await load_setu(s_type)

        elif s_type == SetuModelName.R18:
            return await load_setu(s_type)

    else:
        return {"code": 403, "data": "", "msg": "请停止非法行为！如再继续，达到次数将永久Ban IP！"}


if __name__ == '__main__':
    CONFIG_PATH = Path('.') / 'config.yml'
    config = load_yaml(CONFIG_PATH)['api']
    uvicorn.run(app,
                host=config['host'],
                port=config['port'])
