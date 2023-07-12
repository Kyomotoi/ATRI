import json
from pathlib import Path
from typing import Union
from pip import main as pipmain
from asyncio import as_completed

import nonebot

from ATRI.log import log
from ATRI.utils import request
from ATRI.service import Service, ServiceTools

from .models import NonebotPluginInfo


_NONEBOT_STORE_URLS = [
    "https://registry.nonebot.dev/plugins.json",
    "https://jsd.imki.moe/gh/nonebot/registry@results/plugins.json",
    "https://cdn.staticaly.com/gh/nonebot/registry@results/plugins.json",
    "https://jsd.cdn.zzko.cn/gh/nonebot/registry@results/plugins.json",
    "https://ghproxy.com/https://raw.githubusercontent.com/nonebot/registry/results/plugins.json",
]

_plugin_list = dict()


class NonebotPluginManager:
    _plugin_name = str()
    _conf_path = Path(".") / "nonebot_plugins.json"

    def get_list(self) -> list:
        if not self._conf_path.is_file():
            with open(self._conf_path, "w", encoding="utf-8") as w:
                w.write(json.dumps(list()))

            with open(".env.prod", "w", encoding="utf-8") as w:
                w.write("# 请在此填写来自 Nonebot 商店的插件设置, 填写后需重启以生效")

        return json.loads(self._conf_path.read_bytes())

    def revise_list(self, is_del: bool) -> None:
        data = self.get_list()
        if is_del:
            if self._plugin_name in data:
                data.remove(self._plugin_name)
        else:
            data.append(self._plugin_name)
            data = list(set(data))

        with open(self._conf_path, "w", encoding="utf-8") as w:
            w.write(json.dumps(data))

    def assign_plugin(self, plugin_name: str) -> "NonebotPluginManager":
        self._plugin_name = plugin_name
        return self

    async def get_store_list(self) -> None:
        global _plugin_list

        if not _plugin_list:
            tasks = [request.get(url) for url in _NONEBOT_STORE_URLS]
            for future in as_completed(tasks, timeout=114514):
                try:
                    data = await future
                    _plugin_list = {
                        plugin["module_name"]: plugin for plugin in data.json()
                    }
                    log.success("刷新 Nonebot 商店成功")
                    return
                except Exception:
                    log.warning("刷新 Nonebot 商店失败, 尝试下一个链接")

    def get_plugin_info(self) -> Union[NonebotPluginInfo, None]:
        if plugin_data := _plugin_list.get(self._plugin_name):
            return NonebotPluginInfo.parse_obj(plugin_data)
        else:
            return None

    def plugin_is_exist(self, is_conf: bool = False) -> bool:
        if not is_conf:
            return bool(self.get_plugin_info())
        else:
            return True if self._plugin_name in self.get_list() else False

    def add_plugin(self) -> str:
        if not self.plugin_is_exist():
            return "未找到插件"

        try:
            pipmain(["install", self._plugin_name])
        except Exception:
            return "插件下载失败"

        nonebot.load_plugin(self._plugin_name)
        self.revise_list(False)
        plugin_info = self.get_plugin_info()
        desc = plugin_info.desc + "\n" + plugin_info.homepage  # type: ignore
        Service(self._plugin_name).document(desc).is_nonebot_plugin()

        return "完成~!"

    def remove_plugin(self) -> str:
        if not self.plugin_is_exist():
            return "未找到插件"

        try:
            pipmain(["uninstall", "-y", self._plugin_name])
        except Exception:
            return "插件包卸载失败, 请重启后再尝试"

        self.revise_list(True)
        try:
            ServiceTools(self._plugin_name).del_service()
        except Exception:
            return f"部分完成: 信息文件删除失败, 路径: data/services/{self._plugin_name}.json"
        return "完成~! 将在下次重启生效"

    def upgrade_plugin(self) -> list:
        if not (plugin_list := self.get_list()):
            return list()

        succ_list = list()
        for plugin in plugin_list:
            try:
                pipmain(["install", "--upgrade", plugin])
                succ_list.append(plugin)
                log.success(f"Nonebot 插件 {plugin} 更新成功")
            except Exception:
                log.warning(f"Nonebot 插件 {plugin} 更新失败")

        return succ_list

    def load_plugin(self) -> None:
        plugin_list = self.get_list()
        for plugin in plugin_list:
            nonebot.load_plugin(plugin)
