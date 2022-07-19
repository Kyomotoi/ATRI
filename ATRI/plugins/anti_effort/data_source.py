import json
import re
import os
from pathlib import Path

from ATRI.service import Service
from ATRI.rule import is_in_service
from ATRI.utils import request
from ATRI.log import logger as log

from .models import AntiEffortUserModel


PLUGIN_DIR = Path(".") / "data" / "plugins" / "anti_effort"
PLUGIN_DIR.mkdir(parents=True, exist_ok=True)


class AntiEffort(Service):
    def __init__(self):
        Service.__init__(
            self, "谁是卷王", "谁是卷王！", rule=is_in_service("谁是卷王"), main_cmd="/ae"
        )

    def add_user(self, group_id: int, user_id: int, waka_url: str) -> str:
        patt = r"/@([a-zA-Z0-9].*?)/([a-zA-Z0-9].*?).json"
        match = re.findall(patt, waka_url)
        if not match:
            return "哥，你提供的链接有问题啊"

        w_user_name = match[0][0]
        w_user_id = match[0][1]

        file_path = PLUGIN_DIR / f"{group_id}.json"
        if not file_path.exists():
            with open(file_path, "w") as f:
                f.write(json.dumps(list()))

        data: list = json.loads(file_path.read_text())
        data.append(
            AntiEffortUserModel(
                user_id=user_id,
                w_user_name=w_user_name,
                w_user_id=w_user_id,
                waka_url=waka_url,
                last_7_days_count=int(),
                recent_count=int(),
            ).dict()
        )
        with open(file_path, "w") as f:
            f.write(json.dumps(data))

        return "成功加入卷王统计榜！"

    def del_user(self, group_id: int, user_id: int) -> str:
        data = self.get_data(group_id)
        file_path = PLUGIN_DIR / f"{group_id}.json"
        if file_path.exists():
            for i in data:
                if i["user_id"] == user_id:
                    data.remove(i)
                    with open(PLUGIN_DIR / f"{group_id}.json", "w") as f:
                        f.write(json.dumps(data))
                    return "成功退出卷王统计榜！"

        return "贵群还没有人加入卷王统计榜！"

    def get_data(self, group_id: int) -> list:
        file_path = PLUGIN_DIR / f"{group_id}.json"
        if not file_path.exists():
            return list()
        return json.loads(file_path.read_text())

    def update_user(self, group_id: int, user_id: int, update_map: dict):
        data = self.get_data(group_id)
        if data:
            file_path = PLUGIN_DIR / f"{group_id}.json"
            for i in data:
                if i["user_id"] == user_id:
                    for k, v in update_map.items():
                        i[k] = v
                    with open(file_path, "w") as f:
                        f.write(json.dumps(data))

    async def update_data(self):
        files = os.listdir(PLUGIN_DIR)
        if not files:
            return 114514

        groups = list()
        for f in files:
            group_id = int(f.split(".")[0])
            groups.append(group_id)

        for i in groups:
            data = self.get_data(i)
            if not data:
                continue

            for j in data:
                try:
                    resp = await request.get(j["waka_url"])
                except Exception:
                    log.error(f"获取卷王 {j['user_id']} 数据失败！")
                    continue

                user_w_data = resp.json()  # type: ignore
                d = user_w_data["data"]
                user_w_last_7_days_count = float()
                user_w_recent_count = float(d[-1]["grand_total"]["decimal"])
                for u in d:
                    user_w_last_7_days_count += float(u["grand_total"]["decimal"])

                u_data = {
                    "last_7_days_count": user_w_last_7_days_count,
                    "recent_count": user_w_recent_count,
                }
                self.update_user(i, j["user_id"], u_data)
