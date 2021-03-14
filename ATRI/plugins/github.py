import re
import json
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.service import Service as sv
from ATRI.rule import is_block, is_in_dormant
from ATRI.utils.request import get_bytes
from ATRI.exceptions import RequestTimeOut


URL = "https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"


github_issues = sv.on_message(rule=is_block() & is_in_dormant())
sv.manual_reg_service("GitHubIssue速览")

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
