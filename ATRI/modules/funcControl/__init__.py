import os
import json
from pathlib import Path
from typing import Optional


def checkSwitch(funcName: str, g: int):
    file = Path('.') / 'ATRI' / 'modules' / 'funcControl' / 'ALLswitch.json'
    with open(file, 'r') as f:
        data = json.load(f)
    if data[funcName] == "off":
        return False
    else:
        try:
            file = Path('.') / 'ATRI' / 'data' / 'groupData' / f'{g}' / 'switch.json'
            with open(file, 'r') as f:
                data = json.load(f)
        except:
            try:
                os.mkdir(Path('.') / 'ATRI' / 'data' / 'groupData' / f'{g}')
            except:
                pass
            data = {}
            data["pixiv_seach_img"] = "on"
            data["pixiv_seach_author"] = "on"
            data["pixiv_daily_rank"] = "on"
            data["setu"] = "on"
            data["setu_img"] = "on"
            data["anime_search"] = "on"
            data["change_face"] = "on"
            data["chouYou"] = "on"
            data["saucenao_search"] = "on"
            with open(Path('.') / 'ATRI' / 'data' / 'groupData' / f'{g}' / 'switch.json', 'w') as f:
                f.write(json.dumps(data))
                f.close()
        
        if data[funcName] == "on":
            return True

def checkNoob(u: int, g: Optional[int] = None):
    fileU = Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobList.json'
    fileG = Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobGroup.json'
    try:
        with open(fileU, 'r') as f:
            dataU = json.load(f)
    except:
        dataU = {}

    try:
        with open(fileG, 'r') as f:
            dataG = json.load(f)
    except:
        dataG = {}

    if str(u) not in dataU.keys():
        if g:
            if str(g) not in dataG.keys():
                return True
        else:
            return True
    else:
        pass