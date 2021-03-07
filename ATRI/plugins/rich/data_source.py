#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
File: data_source.py
Created Date: 2021-02-07 09:34:31
Author: Kyomotoi
Email: Kyomotoiowo@gmail.com
License: GPLv3
Project: https://github.com/Kyomotoi/ATRI
--------
Last Modified: Sunday, 7th March 2021 3:14:31 pm
Modified By: Kyomotoi (kyomotoiowo@gmail.com)
--------
Copyright (c) 2021 Kyomotoi
'''

table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr = {}
for i in range(58):
    tr[table[i]] = i
s = [11, 10, 3, 8, 4, 6]
xor = 177451812
add = 8728348608


def dec(x) -> int:
    r = 0
    for i in range(6):
        r += tr[x[s[i]]] * 58**i
    return (r - add) ^ xor


def enc(x) -> str:
    x = (x ^ xor) + add
    r = list('BV1  4 1 7  ')
    for i in range(6):
        r[s[i]] = table[x // 58**i % 58]
    return ''.join(r)
