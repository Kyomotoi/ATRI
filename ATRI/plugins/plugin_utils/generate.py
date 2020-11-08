#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   generateID.py
@Time    :   2020/11/08 10:35:09
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import os
import json
import random
from pathlib import Path
from zipfile import PyZipFile
from typing import Tuple, Dict, List

file = Path('.') / 'ATRI' / 'data' / 'data_IDcard' / 'main.bin'


def infoID() -> Tuple[Dict[str, List[str]], Dict[str, str]]:
    with PyZipFile(os.path.abspath(file), "r") as zipFile:
        with zipFile.open("name.json", "r") as f:
            name = json.loads(f.read().decode())
        with zipFile.open("area.json", "r") as f:
            area = json.loads(f.read().decode())
    return name, area


def numberID(area: int, sex: int, birth: int) -> str:
    def checkSum(fullCode: str) -> int or str:
        assert len(fullCode) == 17
        checkSum = sum([((1 << (17 - i)) % 11) * int(fullCode[i])
                        for i in range(0, 17)])
        checkDigit = (12 - (checkSum % 11)) % 11
        if checkDigit < 10:
            return checkDigit
        else:
            return "X" # type: ignore

    orderCode = str(random.randint(10, 99))
    sexCode = str(random.randrange(sex, 10, step=2))
    fullCode = str(area) + str(birth) + str(orderCode) + str(sexCode)
    fullCode += str(checkSum(fullCode))
    return fullCode
