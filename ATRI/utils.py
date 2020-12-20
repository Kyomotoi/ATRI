import yaml
from datetime import datetime
from pathlib import Path


def loadYaml(file: Path) -> dict:
    '''
    读取yaml文件
    :return: dict
    '''
    with open(file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data


def countList(lst: list, aim) -> int:
    '''
    检查某列表中目标出现的次数
    :return: int
    '''
    count = 0
    for ele in lst:
        if ele == aim:
            count = count + 1
    return count


def delListAim(lst: list, aim) -> list:
    '''
    删除某列表中所有目标元素
    :return: list
    '''
    while aim in lst:
        lst.remove(aim)
    return lst


def nowTime() -> float:
    '''
    获取当前时间（小时）
    :return: float
    '''
    now_ = datetime.now()
    hour = now_.hour
    minute = now_.minute
    now = hour + minute / 60
    return now