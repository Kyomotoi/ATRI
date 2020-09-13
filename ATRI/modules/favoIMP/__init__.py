import json
from random import randint
from pathlib import Path

def GetFavoIMP(u):
    try:
        with open(Path('.') / 'ATRI' / 'modules' / 'favoIMP' / 'user.json', 'r') as f:
            data = json.load(f)
    except:
        return 0
    
    try:
        if data[f"{u}"][0]:
            pass
        else:
            return 0
    except:
        return 0

    return [data[f"{u}"][0], data[f"{u}"][1]]

def AddFavoIMP(u, f:int, s:bool):
    if s:
        favoIMP = randint(1,f)
    else:
        favoIMP = f
        try:
            with open(Path('.') / 'ATRI' / 'modules' / 'favoIMP' / 'user.json', 'r') as a:
                data = json.load(a)
            data[f"{u}"][0] = int(data[f"{u}"][0]) + favoIMP
            with open(Path('.') / 'ATRI' / 'modules' / 'favoIMP' / 'user.json', 'w') as a:
                a.write(json.dumps(data))
                a.close()
        except:
            data = {}
            data[f"{u}"] = [f"{favoIMP}"]
            with open(Path('.') / 'ATRI' / 'modules' / 'favoIMP' / 'user.json', 'w') as a:
                a.write(json.dumps(data))
                a.close()

def DelFavoIMP(u, f:int, s:bool):
    if s:
        favoIMP = randint(1,f)
    else:
        favoIMP = f
        try:
            with open(Path('.') / 'ATRI' / 'modules' / 'favoIMP' / 'user.json', 'r') as a:
                data = json.load(a)
            data[f"{u}"][0] = int(data[f"{u}"][0]) - favoIMP
            with open(Path('.') / 'ATRI' / 'modules' / 'favoIMP' / 'user.json', 'w') as a:
                a.write(json.dumps(data))
                a.close()
        except:
            data = {}
            data[f"{u}"] = [f"{0 - favoIMP}"]
            with open(Path('.') / 'ATRI' / 'modules' / 'favoIMP' / 'user.json', 'w') as a:
                a.write(json.dumps(data))
                a.close()