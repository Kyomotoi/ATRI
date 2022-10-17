from pathlib import Path

from nonebot.adapters.onebot.v11 import MessageEvent

from ATRI.permission import ADMIN
from ATRI.service import Service
from ATRI.message import MessageBuilder


RSS_PLUGIN_DIR = Path(".") / "ATRI" / "plugins" / "rss"


rss_helper = (
    Service("rss")
    .document("Rss系插件助手")
    .only_admin(True)
    .permission(ADMIN)
    .main_cmd("/rss")
)


rss_menu = rss_helper.on_command("/rss", "Rss帮助菜单")


@rss_menu.handle()
async def _rss_menu(event: MessageEvent):
    raw_rss_list = RSS_PLUGIN_DIR.glob("rss_*")
    rss_list = [str(i).split("/")[-1] for i in raw_rss_list]
    if not rss_list:
        rss_list = [str(i).split("\\")[-1] for i in raw_rss_list]

    result = (
        MessageBuilder("Rss Helper:")
        .text(f"可用订阅源: {', '.join(map(str, rss_list)).replace('rss_', str())}")
        .text("命令: /rss.(订阅源名称)")
    )
    await rss_menu.finish(result)
