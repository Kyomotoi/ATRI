#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   genshin.py
@Time    :   2020/11/07 22:34:58
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
@Docs    :   Fork from https://github.com/Womsxd/YuanShen_User_Info
'''
__author__ = 'kyomotoi'

import json
import time
import string
import random
import hashlib
import requests


def md5(text: str) -> str:
    """text 转 md5"""
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


def DSGet() -> str:
    mhyVersion = "2.1.0"
    n = md5(mhyVersion)
    i = str(int(time.time()))
    r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
    c = md5("salt=" + n + "&t=" + i + "&r=" + r)
    return i + "," + r + "," + c


def GetInfo(uid: str) -> str:
    """请求API"""
    req = requests.get(
        url=
        f"https://api-takumi.mihoyo.com/game_record/genshin/api/index?server=cn_gf01&role_id={uid}",
        headers={
            'Accept': 'application/json, text/plain, */*',
            'DS': DSGet(),
            'Origin': 'https://webstatic.mihoyo.com',
            'x-rpc-app_version': '2.1.0',
            'User-Agent':
            'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/2.2.0',
            'x-rpc-client_type': '4',
            'Referer':
            'https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'X-Requested-With': 'com.mihoyo.hyperion'
        })
    return req.text


def JsonAnalysis(JsonText) -> str:
    """解析数据"""
    data = json.loads(JsonText)

    Character_Info = "Roles:\n"
    Character_List = []
    Character_List = data["data"]["avatars"]
    for i in Character_List:
        if (i["element"] == "None"):
            Character_Type = "无属性"
        elif (i["element"] == "Anemo"):
            Character_Type = "风属性"
        elif (i["element"] == "Pyro"):
            Character_Type = "火属性"
        elif (i["element"] == "Geo"):
            Character_Type = "岩属性"
        elif (i["element"] == "Electro"):
            Character_Type = "雷属性"
        elif (i["element"] == "Cryo"):
            Character_Type = "冰属性"
        elif (i["element"] == "Hydro"):
            Character_Type = "水属性"
        else:
            Character_Type = "草属性"

        if (i["name"] == "旅行者"):
            if (i["image"].find("UI_AvatarIcon_PlayerGirl") != -1):
                TempText = f'* {i["name"]}：\n'
                TempText += f'  - [萤——妹妹] {i["level"]}级 {Character_Type}\n'

            elif (i["image"].find("UI_AvatarIcon_PlayerBoy") != -1):
                TempText = f'* {i["name"]}：\n'
                TempText += f'  - [空——哥哥] {i["level"]}级 {Character_Type}\n'

            else:
                TempText = f'* {i["name"]}：\n'
                TempText += f'  - [性别判断失败] {i["level"]}级 {Character_Type}\n'
        else:
            TempText = f'* {i["name"]} {i["rarity"]}★角色:\n'
            TempText += f'  - {i["level"]}级 好感度({i["fetter"]})级 {Character_Type}\n'

        Character_Info = Character_Info + TempText

    a1 = data["data"]["stats"]["spiral_abyss"]

    Account_Info = 'Account Info:\n'
    Account_Info += f'- 活跃天数：{data["data"]["stats"]["active_day_number"]} 天\n'
    Account_Info += f'- 达成成就：{data["data"]["stats"]["achievement_number"]} 个\n'
    Account_Info += f'- 获得角色：{data["data"]["stats"]["avatar_number"]}个\n'
    Account_Info += f'- 深渊螺旋：{"没打" if (data["data"]["stats"]["spiral_abyss"] == "-") else f"打到了{a1}"}\n'
    Account_Info += f'* 收集：\n'
    Account_Info += f'  - 风神瞳{data["data"]["stats"]["anemoculus_number"]}个 岩神瞳{data["data"]["stats"]["geoculus_number"]}个\n'
    Account_Info += f'* 解锁：\n'
    Account_Info += f'  - 传送点{data["data"]["stats"]["way_point_number"]}个 秘境{data["data"]["stats"]["domain_number"]}个\n'
    Account_Info += f'* 共开启宝箱：\n'
    Account_Info += f'  - 普通：{data["data"]["stats"]["common_chest_number"]}个 精致：{data["data"]["stats"]["exquisite_chest_number"]}个\n'
    Account_Info += f'  - 珍贵：{data["data"]["stats"]["luxurious_chest_number"]}个 华丽：{data["data"]["stats"]["precious_chest_number"]}个'

    print(Character_Info + "\r\n" + Account_Info)
    return Character_Info + "\r\n" + Account_Info