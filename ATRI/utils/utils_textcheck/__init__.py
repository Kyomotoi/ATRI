#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   data_source.py
@Time    :   2020/11/21 19:54:11
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import json
from pathlib import Path
from typing import Optional

PUBLIC_OPINION_PATH = Path('.') / 'ATRI' / 'utils' / 'utils_textcheck' / 'public_opinion.json'


class Textcheck:
    """文字检查，专供舆情"""
    with open(PUBLIC_OPINION_PATH, 'r+') as f:
        try:
            data = json.load(f)
        except:
            data = {}

    def check(self, msg: str) -> Optional[str]:
        wait_list = [keys for keys in self.data.keys()]
        for word in wait_list:
            if word in msg:
                return self.data[word]
            else:
                return "False"

    def add_word(self, word: str, repo: str, max_times: int,
                 ban_time: int) -> Optional[str]:
        if word in self.data:
            return '相关关键词已经有啦~！'
        else:
            self.data[word] = [repo, max_times, ban_time]
            msg0 = '学習しました！\n'
            msg0 += f'Key: {word}\n'
            msg0 += f'Repo: {repo}\n'
            msg0 += f'Max times: {max_times}\n'
            msg0 += f'Ban time: {ban_time}'
            return msg0
    
    def del_word(self, word: str) -> str:
        if word in self.data:
            del self.data[word]
            return "好叻~！"
        else:
            return "未发现相关关键词呢..."
    
    def get_times(self, word: str) -> Optional[int]:
        if word not in self.data:
            return 0
        else:
            return self.data[word][1]
