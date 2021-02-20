"""
Idea from: https://github.com/cczu-osa/aki
"""
import json
from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.rule import is_in_banlist, is_in_dormant
from ATRI.utils.request import post_bytes
from ATRI.exceptions import RequestTimeOut


RUN_API_URL_FORMAT = 'https://glot.io/run/{}?version=latest'
SUPPORTED_LANGUAGES = {
    'assembly': {'ext': 'asm'},
    'bash': {'ext': 'sh'},
    'c': {'ext': 'c'},
    'clojure': {'ext': 'clj'},
    'coffeescript': {'ext': 'coffe'},
    'cpp': {'ext': 'cpp'},
    'csharp': {'ext': 'cs'},
    'erlang': {'ext': 'erl'},
    'fsharp': {'ext': 'fs'},
    'go': {'ext': 'go'},
    'groovy': {'ext': 'groovy'},
    'haskell': {'ext': 'hs'},
    'java': {'ext': 'java', 'name': 'Main'},
    'javascript': {'ext': 'js'},
    'julia': {'ext': 'jl'},
    'kotlin': {'ext': 'kt'},
    'lua': {'ext': 'lua'},
    'perl': {'ext': 'pl'},
    'php': {'ext': 'php'},
    'python': {'ext': 'py'},
    'ruby': {'ext': 'rb'},
    'rust': {'ext': 'rs'},
    'scala': {'ext': 'scala'},
    'swift': {'ext': 'swift'},
    'typescript': {'ext': 'ts'},
}


code_runner = on_command("/code", rule=is_in_banlist() & is_in_dormant())

@code_runner.handle()
async def _code_runner(bot: Bot, event: MessageEvent) -> None:
    msg = str(event.message).split("\n")
    laug = msg[0].replace("\r", "")
    if laug not in SUPPORTED_LANGUAGES:
        await code_runner.finish("该语言暂不支持...")
    
    code = msg[1]
    try:
        req = await post_bytes(
            RUN_API_URL_FORMAT.format(laug),
            json={
                "files": [{
                        "name": (SUPPORTED_LANGUAGES[laug].get("name", "main") +
                        f".{SUPPORTED_LANGUAGES[laug]['ext']}"),
                        "content": code
                }],
                "stdin": "",
                "command": ""
            }
        )
    except RequestTimeOut:
        raise RequestTimeOut("Failed to request!")
    
    payload = json.loads(req)
    sent = False
    for k in ['stdout', 'stderr', 'error']:
        v = payload.get(k)
        lines = v.splitlines()
        lines, remained_lines = lines[:10], lines[10:]
        out = '\n'.join(lines)
        out, remained_out = out[:60 * 10], out[60 * 10:]

        if remained_lines or remained_out:
            out += f"\n（输出过多，已忽略剩余内容）"

        if out:
            await bot.send(event, f"{k}:\n\n{out}")
            sent = True
    
    if not sent:
        await code_runner.finish("运行完成，没有任何输出")
