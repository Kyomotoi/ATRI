#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   data_source.py
@Time    :   2020/11/21 11:13:42
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import re
import os
import time
import json
import string
import random
import hashlib
import requests
from pathlib import Path
from zipfile import PyZipFile
from typing import Tuple, Dict, List


class Generate:
    """虚拟身份证部分"""
    GENERATE_DATA_PATH = Path(
        '.') / 'ATRI' / 'plugins' / 'plugin_utils' / 'main.bin'

    def infoID(self) -> Tuple[Dict[str, List[str]], Dict[str, str]]:
        with PyZipFile(os.path.abspath(self.GENERATE_DATA_PATH),
                       "r") as zipFile:
            with zipFile.open("name.json", "r") as f:
                name = json.loads(f.read().decode())
            with zipFile.open("area.json", "r") as f:
                area = json.loads(f.read().decode())
        return name, area

    def numberID(self, area: int, sex: int, birth: int) -> str:
        def checkSum(fullCode: str) -> int or str:
            assert len(fullCode) == 17
            checkSum = sum([((1 << (17 - i)) % 11) * int(fullCode[i])
                            for i in range(0, 17)])
            checkDigit = (12 - (checkSum % 11)) % 11
            if checkDigit < 10:
                return checkDigit
            else:
                return "X"  # type: ignore

        orderCode = str(random.randint(10, 99))
        sexCode = str(random.randrange(sex, 10, step=2))
        fullCode = str(area) + str(birth) + str(orderCode) + str(sexCode)
        fullCode += str(checkSum(fullCode))
        return fullCode


class Genshin:
    """原神部分"""
    def md5(self, text: str) -> str:
        """text 转 md5"""
        md5 = hashlib.md5()
        md5.update(text.encode())
        return md5.hexdigest()

    def DSGet(self) -> str:
        mhyVersion = "2.1.0"
        n = self.md5(mhyVersion)
        i = str(int(time.time()))
        r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
        c = self.md5("salt=" + n + "&t=" + i + "&r=" + r)
        return i + "," + r + "," + c

    def GetInfo(self, uid: str) -> str:
        """请求API"""
        req = requests.get(
            url=
            f"https://api-takumi.mihoyo.com/game_record/genshin/api/index?server=cn_gf01&role_id={uid}",
            headers={
                'Accept': 'application/json, text/plain, */*',
                'DS': self.DSGet(),
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

    def JsonAnalysis(self, JsonText) -> str:
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

        return Character_Info + "\r\n" + Account_Info


class Roll:
    """骰娘部分"""
    def roll_dice(self, par: str) -> str:
        """掷骰子"""
        result = 0
        proc = ''
        proc_list = []
        p = par.split('+')

        # 计算每个单独的roll
        for i in p:
            args = re.findall(r"(\d{0,10})(?:(d)(\d{1,10}))", i)
            args = list(args[0])

            if not args[0]:
                args[0] = 1

            if int(args[0]) >= 5000 or int(args[2]) >= 5000:
                return '阿..好大...'

            for a in range(1, int(args[0]) + 1):
                rd = random.randint(1, int(args[2]))
                result = result + rd

                if len(proc_list) <= 10:
                    proc_list.append(rd)

        if len(proc_list) <= 10:
            proc += "+".join(map(str, proc_list))

        elif len(proc_list) >= 10:
            proc += '太长了不展示了就酱'

        else:
            proc += str(result)

        result = f"{par}=({proc})={result}"

        return str(result)