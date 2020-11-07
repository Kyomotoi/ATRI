#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/11/06 22:26:06
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import yaml
from pathlib import Path


def load_yaml(file: Path) -> dict:
    '''
    读取yaml文件

    :return: dict
    '''
    with open(file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data
