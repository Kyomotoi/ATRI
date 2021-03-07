#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
File: github.py
Created Date: 2021-02-26 23:22:34
Author: Kyomotoi
Email: Kyomotoiowo@gmail.com
License: GPLv3
Project: https://github.com/Kyomotoi/ATRI
--------
Last Modified: Sunday, 7th March 2021 3:11:56 pm
Modified By: Kyomotoi (kyomotoiowo@gmail.com)
--------
Copyright (c) 2021 Kyomotoi
'''

import re
import json

from nonebot.plugin import on_message
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.rule import is_in_banlist, is_in_dormant
from ATRI.utils.request import get_bytes
from ATRI.exceptions import RequestTimeOut


URL = "https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"


github_issues = on_message(rule=is_in_banlist() & is_in_dormant())

@github_issues.handle()
async def _github_issues(bot: Bot, event: MessageEvent) -> None:
    msg = str(event.message)
    patt = r"https://github.com/(.*)/(.*)/issues/(.*)"
    need_info = re.findall(patt, msg)
    if not need_info:
        return
    
    for i in need_info:
        need_info = list(i)
        owner = need_info[0]
        repo = need_info[1]
        issue_number = need_info[2]
        url = URL.format(owner=owner,
                         repo=repo,
                         issue_number=issue_number)
        
        try:
            data = await get_bytes(url)
        except RequestTimeOut:
            return
        
        data = json.loads(data)
        msg0 = (
            f"{repo}: #{issue_number} {data['state']}\n"
            f"comments: {data['comments']}\n"
            f"update: {data['updated_at']}\n"
            f"{data['body']}"
        )
        await github_issues.finish(msg0)
