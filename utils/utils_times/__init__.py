#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/10/31 19:36:49
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import warnings


def countX(lst: list, aim) -> int:
    '''
    检查某列表某元素出现次数

    :return: int
    '''
    warnings.simplefilter('ignore', ResourceWarning)
    count = 0
    for ele in lst:
        if (ele == aim):
            count = count + 1
    return count