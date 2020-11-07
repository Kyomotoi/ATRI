#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   roll.py
@Time    :   2020/11/07 15:56:02
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import re
from random import randint


def roll_dice(par: str) -> str:
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
            rd = randint(1, int(args[2]))
            result = result + rd

            if len(proc_list) <= 10:
                proc_list.append(rd)

    if len(proc_list) == 10:
        temp_list = []
        for i in proc_list:
            if len(temp_list) == 9:
                proc += str(i)
            else:
                proc += str(i) + '+'
                temp_list.append(i)

    elif len(proc_list) >= 10:
        proc += '太长了不展示了'
    
    else:
        proc += str(result)

    result = f"{par}=({proc})={result}"

    return str(result)
