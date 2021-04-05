import os
import json
from pathlib import Path
from typing import Optional


KEYREPO_DIV = Path('.') / 'ATRI' / 'data' / 'database' / 'KeyRepo'
os.makedirs(KEYREPO_DIV, exist_ok=True)


def load_key_data() -> dict:
    file_name = "data.json"
    path = KEYREPO_DIV / file_name
    try:
        data = json.loads(path.read_bytes())
    except:
        with open(path, 'w') as r:
            r.write(json.dumps({}))
        data = {}
    return data


def load_key_temp_data() -> list:
    file_name = "data.temp.json"
    path = KEYREPO_DIV / file_name
    try:
        data = json.loads(path.read_bytes())
    except:
        with open(path, 'w') as r:
            r.write(json.dumps([]))
        data = []
    return data


def load_key_history() -> list:
    file_name = "data.history.json"
    path = KEYREPO_DIV / file_name
    try:
        data = json.loads(path.read_bytes())
    except:
        with open(path, 'w') as r:
            r.write(json.dumps([]))
        data = []
    return data


def save_key_data(d: dict) -> None:
    file_name = "data.json"
    path = KEYREPO_DIV / file_name
    with open(path, 'w') as r:
        r.write(json.dumps(d))


def save_key_temp_data(d: list) -> None:
    file_name = "data.temp.json"
    path = KEYREPO_DIV / file_name
    with open(path, 'w') as r:
        r.write(json.dumps(d))


def save_key_history_data(d: list) -> None:
    file_name = "data.history.json"
    path = KEYREPO_DIV / file_name
    with open(path, 'w') as r:
        r.write(json.dumps(d))


def add_key(key: str, repo: str) -> str:
    data = load_key_data()
    data_1 = data.get(key, [])
    if repo in data_1:
        return "该回复已存在~！"
    data_1.append(repo)
    data[key] = data_1
    save_key_data(data)
    return "成功，又学到新知识了~！"


def add_key_temp(d: dict) -> None:
    data: list = load_key_temp_data()
    data.append(d)
    save_key_temp_data(data)
    add_history(d, False)


def add_history(d: dict, p: bool = True) -> None:
    d['pass'] = p
    data: list = load_key_history()
    data.append(d)
    save_key_history_data(data)


def del_key(key: str, repo: str) -> str:
    data = load_key_data()
    if repo == 'isALL':
        del data[key]
        msg = f"成功删除关键词[{key}]下所有回复..."
    else:
        data_1 = data.get(key, [])
        try:
            data_1.remove(key)
        except KeyError:
            raise KeyError('Find repo error.')
        data[key] = data_1
        msg = f"成功删除关键词[{key}]下回复：{repo}"
    save_key_data(data)
    return msg


def del_key_temp(d: dict) -> bool:
    data = load_key_temp_data()
    if d in data:
        data.remove(d)
        return True
    else:
        return False
