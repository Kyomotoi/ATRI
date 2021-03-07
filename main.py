#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
File: main.py
Created Date: 2021-02-02 15:51:30
Author: Kyomotoi
Email: Kyomotoiowo@gmail.com
License: GPLv3
Project: https://github.com/Kyomotoi/ATRI
--------
Last Modified: Sunday, 7th March 2021 12:25:07 pm
Modified By: Kyomotoi (kyomotoiowo@gmail.com)
--------
Copyright (c) 2021 Kyomotoi
'''

import ATRI

ATRI.init()
app = ATRI.asgi()

if __name__ == '__main__':
    ATRI.run('main:app')
