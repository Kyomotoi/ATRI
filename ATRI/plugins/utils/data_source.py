#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
File: data_source.py
Created Date: 2021-02-04 21:14:59
Author: Kyomotoi
Email: Kyomotoiowo@gmail.com
License: GPLv3
Project: https://github.com/Kyomotoi/ATRI
--------
Last Modified: Sunday, 7th March 2021 3:14:22 pm
Modified By: Kyomotoi (kyomotoiowo@gmail.com)
--------
Copyright (c) 2021 Kyomotoi
'''

import re
import random


def roll_dice(par: str) -> str:
    result = 0
    proc = ''
    proc_list = []
    p = par.split("+")
    
    for i in p:
        args = re.findall(r"(\d{0,10})(?:(d)(\d{1,10}))", i)
        args = list(args[0])
        
        args[0] = args[0] or 1
        if int(args[0]) >= 5000 or int(args[2]) >= 5000:
            return "阿...好大......"
        
        for a in range(1, int(args[0]) + 1):
            rd = random.randint(1, int(args[2]))
            result = result + rd
            
            if len(proc_list) <= 10:
                proc_list.append(rd)
    
    if len(proc_list) <= 10:
        proc += "+".join(map(str, proc_list))
    elif len(proc_list) > 10:
        proc += "太长了不展示了就酱w"
    else:
        proc += str(result)
    
    result = f"{par}=({proc})={result}"
    return result
