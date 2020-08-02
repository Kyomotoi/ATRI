# -*- coding:utf-8 -*-
import sqlite3

from fastapi import FastAPI
from enum import Enum


app = FastAPI()
path_setu = f'ATRI\\splite\\setu\\'
path_cloudmusic = f'ATRI\\splite\\cloudmusic\\'

class ModelName(str, Enum):
    alexnet = "normal"
    resnet = "nearR18"
    lenet = "r18"


@app.get("/setu/{h_type}")
def get_setu(h_type: str):
    if h_type == ModelName.alexnet:
        con = sqlite3.connect(path_setu + 'normal.db')
        cur = con.cursor()
        msg = cur.execute('SELECT * FROM normal ORDER BY RANDOM() limit 1;')
        for i in msg:
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
            return {"Pid": pid, 0:{"title": title,"tags": tags,"account": account, "name": name,"u_id": u_id, "user_link": user_link, "img": img}}
    
    elif h_type == ModelName.resnet:
        con = sqlite3.connect(path_setu + 'nearR18.db')
        cur = con.cursor()
        msg = cur.execute('SELECT * FROM nearR18 ORDER BY RANDOM() limit 1;')
        for i in msg:
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
            return {"Pid": pid, 0:{"title": title,"tags": tags,"account": account, "name": name,"u_id": u_id, "user_link": user_link, "img": img}}

    elif h_type == ModelName.lenet:
        con = sqlite3.connect(path_setu + 'r18.db')
        cur = con.cursor()
        msg = cur.execute('SELECT * FROM r18 ORDER BY RANDOM() limit 1;')
        for i in msg:
            pid = i[0]
            title = i[1]
            tags = i[2]
            account = i[3]
            name = i[4]
            u_id = i[5]
            user_link = i[6]
            img = i[7]
            con.commit()
            con.close()
            return {"Pid": pid, 0:{"title": title,"tags": tags,"account": account, "name": name,"u_id": u_id, "user_link": user_link, "img": img}}


@app.get("/cloudmusic")
async def Depression():
    con = sqlite3.connect(path_cloudmusic + 'cloudmusic.db')
    cur = con.cursor()
    msg = cur.execute('SELECT * FROM cloudmusic ORDER BY RANDOM() limit 1;')
    for i in msg:
        msg = i[0]
        con.commit()
        con.close()
        return {"msg": msg}