from pathlib import Path

from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import GROUP_OWNER, GROUP_ADMIN

from ATRI.service import Service


RSS_PLUGIN_DIR = Path(".") / "ATRI" / "plugins" / "rss"


class RssHelper(Service):
    def __init__(self):
        Service.__init__(
            self,
            "rss",
            "Rss系插件助手",
            True,
            permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN,
            main_cmd="/rss",
        )


rss_menu = RssHelper().on_command("/rss", "Rss帮助菜单")


@rss_menu.handle()
async def _rss_menu(event: MessageEvent):
    raw_rss_list = RSS_PLUGIN_DIR.glob("rss_*")
    rss_list = [str(i).split("/")[-1] for i in raw_rss_list]
    if not rss_list:
        rss_list = [str(i).split("\\")[-1] for i in raw_rss_list]

    result = f"""Rss Helper:
    可用订阅源: {"、".join(map(str, rss_list)).replace("rss_", str())}
    命令: /rss.(订阅源名称)
    """.strip()
    await rss_menu.finish(result)
