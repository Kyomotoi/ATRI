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
        file = Path('.') / 'ATRI' / 'data' / 'groupData' / f'{g}' / 'switch.json'
        with open(file, 'r') as f:
            data = json.load(f)
        
        if data[funcName] == "on":
            return True

def checkNoob(user: int, group: Optional[int] = None):
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

    if str(user) not in dataU.keys():
        if group:
            if str(group) not in dataG.keys():
                return True
        else:
            return True
    else:
        pass