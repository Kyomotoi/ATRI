#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import ATRI

ATRI.init()
app = ATRI.asgi()

if __name__ == "__main__":
    ATRI.run("main:app")
