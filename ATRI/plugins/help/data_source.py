import os
import json

from tabulate import tabulate

from ATRI import __version__
from ATRI.rule import to_bot
from ATRI.service import Service, SERVICES_DIR, ServiceTools
from ATRI.config import BotSelfConfig


SERVICE_INFO_FORMAT = """
服务名：{service}
说明：{docs}
可用命令：\n    {cmd_list}
是否全局启用：{enabled}
Tip: @bot 帮助 [服务] [命令] 以查看对应命令详细信息
""".strip()

COMMAND_INFO_FORMAT = """
命令：{cmd}
类型：{cmd_type}
说明：{docs}
更多触发方式：{aliases}
""".strip()


class Helper(Service):
    def __init__(self):
        Service.__init__(self, "帮助", "bot的食用指南~", rule=to_bot())

    @staticmethod
    def menu() -> str:
        return (
            "哦呀？~需要帮助？\n"
            "关于 -查看bot基本信息\n"
            "服务列表 -以查看所有可用服务\n"
            "帮助 [服务] -以查看对应服务帮助\n"
            "Tip: 均需要at触发。@bot 菜单 以打开此页面"
        )

    @staticmethod
    def about() -> str:
        temp_list = list()
        for i in BotSelfConfig.nickname:
            temp_list.append(i)
        nickname = "、".join(map(str, temp_list))
        return (
            "唔...是来认识咱的么\n"
            f"可以称呼咱：{nickname}\n"
            f"咱的型号是：{__version__}\n"
            "想进一步了解：\n"
            "atri.kyomotoi.moe\n"
            "进不去: project-atri-docs.vercel.app"
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
        repo = f"咱搭载了以下服务~\n{table}\n@bot 帮助 [服务] -以查看对应服务帮助"
        return repo

    @staticmethod
    def service_info(service: str) -> str:
        try:
            data = ServiceTools().load_service(service)
        except Exception:
            return "请检查是否输入错误呢...@bot 帮助 [服务]"

        service_name = data.get("service", "error")
        service_docs = data.get("docs", "error")
        service_enabled = data.get("enabled", True)

        _service_cmd_list = list(data.get("cmd_list", {"error"}))
        service_cmd_list = "\n".join(map(str, _service_cmd_list))

        repo = SERVICE_INFO_FORMAT.format(
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

        cmd_list: dict = data["cmd_list"]
        cmd_info = cmd_list.get(cmd, dict())
        if not cmd_info:
            return "请检查命令是否输入错误..."
        cmd_type = cmd_info.get("type", "ignore")
        docs = cmd_info.get("docs", "ignore")
        aliases = cmd_info.get("aliases", "ignore")

        repo = COMMAND_INFO_FORMAT.format(
            cmd=cmd, cmd_type=cmd_type, docs=docs, aliases=aliases
        )
        return repo
