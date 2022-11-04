import os
import json

from tabulate import tabulate

from ATRI import __version__, conf
from ATRI.message import MessageBuilder
from ATRI.service import SERVICES_DIR, ServiceTools


_SERVICE_INFO_FORMAT = (
    MessageBuilder("服务名：{service}")
    .text("说明：{docs}")
    .text("可用命令：\n{cmd_list}")
    .text("是否全局启用：{enabled}")
    .text("Tip: @bot 帮助 (服务) (命令) 以查看对应命令详细信息")
    .done()
)
_COMMAND_INFO_FORMAT = (
    MessageBuilder("命令：{cmd}")
    .text("类型：{cmd_type}")
    .text("说明：{docs}")
    .text("更多触发方式：{aliases}")
    .done()
)


class Helper:
    @staticmethod
    def menu() -> str:
        return (
            MessageBuilder("哦呀?~需要帮助?")
            .text("关于 查看bot基本信息")
            .text("服务列表 -以查看所有可用服务")
            .text("帮助 (服务) -以查看对应服务帮助")
            .text("Tip: 均需要at触发。@bot 菜单 以打开此页面")
            .done()
        )

    @staticmethod
    def about() -> str:
        temp_list = list()
        for i in conf.BotConfig.nickname:
            temp_list.append(i)
        nickname = "、".join(map(str, temp_list))
        return (
            MessageBuilder("唔...是来认识咱的么")
            .text(f"可以称呼咱：{nickname}")
            .text(f"咱的型号是：{__version__}")
            .text("想进一步了解:")
            .text("atri.imki.moe")
            .text("进不去: project-atri-docs.vercel.app")
            .done()
        )

    @staticmethod
    def service_list() -> str:
        files = os.listdir(SERVICES_DIR)
        services = list()
        for f in files:
            prefix = f.replace(".json", "")
            f = os.path.join(SERVICES_DIR, f)
            with open(f, "r", encoding="utf-8") as r:
                service = json.load(r)
                services.append(
                    [
                        prefix,
                        "√" if service["enabled"] else "×",
                        "√" if service["only_admin"] else "×",
                    ]
                )
        table = tabulate(
            services,
            headers=["服务名称", "开启状态(全局)", "仅支持管理员"],
            tablefmt="plain",
        )
        return (
            MessageBuilder("咱搭载了以下服务~")
            .text(table)
            .text("@bot 帮助 (服务) -以查看对应服务帮助")
            .done()
        )

    @staticmethod
    def service_info(service: str) -> str:
        try:
            data = ServiceTools().load_service(service)
        except Exception:
            return "请检查是否输入错误呢...@bot 帮助 (服务)"

        service_name = data.service
        service_docs = data.docs
        service_enabled = data.enabled

        _service_cmd_list = list(data.cmd_list)
        service_cmd_list = "\n".join(map(str, _service_cmd_list))

        repo = _SERVICE_INFO_FORMAT.format(
            service=service_name,
            docs=service_docs,
            cmd_list=service_cmd_list,
            enabled=service_enabled,
        )
        return repo

    @staticmethod
    def cmd_info(service: str, cmd: str) -> str:
        try:
            data = ServiceTools().load_service(service)
        except Exception:
            return "请检查是否输入错误..."

        cmd_list: dict = data.cmd_list
        cmd_info = cmd_list.get(cmd, dict())
        if not cmd_info:
            return "请检查命令是否输入错误..."
        cmd_type = cmd_info.get("type", "ignore")
        docs = cmd_info.get("docs", "ignore")
        aliases = cmd_info.get("aliases", "ignore")

        repo = _COMMAND_INFO_FORMAT.format(
            cmd=cmd, cmd_type=cmd_type, docs=docs, aliases=aliases
        )
        return repo
