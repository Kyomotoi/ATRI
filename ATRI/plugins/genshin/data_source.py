import time
import json
import random
import string
import hashlib
import requests
from typing import Optional

from ATRI.request import Request
from ATRI.config import GENSHIN_CONFIG
from ATRI.exceptions import InvalidRequestError


mhyVersion = GENSHIN_CONFIG['genshin']['mhyVersion']


class Genshin:
    def md5(self, text: str) -> str:
        md5 = hashlib.md5()
        md5.update(text.encode())
        return md5.hexdigest()

    def getDS(self):
        global mhyVersion
        if mhyVersion == '2.1.0':
            n = self.md5(mhyVersion)
        elif mhyVersion == '2.2.1':
            n = "cx2y9z9a29tfqvr1qsq6c7yz99b5jsqt"
        else:
            mhyVersion = "2.2.1"
            n = "cx2y9z9a29tfqvr1qsq6c7yz99b5jsqt"
        
        i = str(int(time.time()))
        r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
        c = self.md5("salt=" + n + "&t="+ i + "&r=" + r)
        return (i + "," + r + "," + c)
    
    def getInfo(self, server_id: str, uid: str) -> str:
        try:
            url = GENSHIN_CONFIG['genshin']['url'] + server_id + "&role_id=" + uid
            print(url)
            headers: dict = {
                'Accept': 'application/json, text/plain, */*',
                'DS': self.getDS(),
                'Origin': 'https://webstatic.mihoyo.com',
                'x-rpc-app_version': mhyVersion,
                'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/2.2.0',
                'x-rpc-client_type': '4',
                'Referer': 'https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,en-US;q=0.8',
                'X-Requested-With': 'com.mihoyo.hyperion'
            }
            result = requests.get(url=url,headers=headers, timeout=10)
            print(result.text)
            return result.text
        except InvalidRequestError:
            raise InvalidRequestError('请求数据出错')
    
    def jsonAnalysis(self, a) -> Optional[str]:
        print(a)
        data = json.loads(a)
        if data['retcode'] != 0:
            raise InvalidRequestError('请求出错，原因：uid错误/不存在/国服之外')
        else:
            pass
        
        character_info = 'Roles:\n'
        character_list = data['data']['avatars']
        for i in character_list:
            if i["element"] == "None":
                character_type = "无属性"
            elif i["element"] == "Anemo":
                character_type = "风属性"
            elif i["element"] == "Pyro":
                character_type = "火属性"
            elif i["element"] == "Geo":
                character_type = "岩属性"
            elif i["element"] == "Electro":
                character_type = "雷属性"
            elif i["element"] == "Cryo":
                character_type = "冰属性"
            elif i["element"] == "Hydro":
                character_type = "水属性"
            else:
                character_type = "草属性"
            
            if i["name"] == "旅行者":
                if i["image"].find("UI_AvatarIcon_PlayerGirl") != -1:
                    temp_text = f'* {i["name"]}：\n'
                    temp_text += f'  - [萤——妹妹] {i["level"]}级 {character_type}\n'

                elif i["image"].find("UI_AvatarIcon_PlayerBoy") != -1:
                    temp_text = f'* {i["name"]}：\n'
                    temp_text += f'  - [空——哥哥] {i["level"]}级 {character_type}\n'

                else:
                    temp_text = f'* {i["name"]}：\n'
                    temp_text += f'  - [性别判断失败] {i["level"]}级 {character_type}\n'
            else:
                temp_text = f'* {i["name"]} {i["rarity"]}★角色:\n'
                temp_text += f'  - {i["level"]}级 好感度({i["fetter"]})级 {character_type}\n'
            
            character_info += temp_text
            
            a1 = data["data"]["stats"]["spiral_abyss"]

            account_info = 'Account Info:\n'
            account_info += f'- 活跃天数：{data["data"]["stats"]["active_day_number"]} 天\n'
            account_info += f'- 达成成就：{data["data"]["stats"]["achievement_number"]} 个\n'
            account_info += f'- 获得角色：{data["data"]["stats"]["avatar_number"]}个\n'
            account_info += f'- 深渊螺旋：{"没打" if (data["data"]["stats"]["spiral_abyss"] == "-") else f"打到了{a1}"}\n'
            account_info += f'* 收集：\n'
            account_info += f'  - 风神瞳{data["data"]["stats"]["anemoculus_number"]}个 岩神瞳{data["data"]["stats"]["geoculus_number"]}个\n'
            account_info += f'* 解锁：\n'
            account_info += f'  - 传送点{data["data"]["stats"]["way_point_number"]}个 秘境{data["data"]["stats"]["domain_number"]}个\n'
            account_info += f'* 共开启宝箱：\n'
            account_info += f'  - 普通：{data["data"]["stats"]["common_chest_number"]}个 精致：{data["data"]["stats"]["exquisite_chest_number"]}个\n'
            account_info += f'  - 珍贵：{data["data"]["stats"]["luxurious_chest_number"]}个 华丽：{data["data"]["stats"]["precious_chest_number"]}个'
            
            return str(character_info + '\r\n' + account_info)
