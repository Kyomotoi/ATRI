import re
import os
import json
from pathlib import Path
from datetime import datetime
from tabulate import tabulate

from ATRI import driver
from ATRI.service import ServiceTools
from ATRI.utils import request
from ATRI.log import log

from .image_dealer import image_dealer
from .models import AntiEffortModel, AntiEffortUserModel


TENCENT_AVATER_URL = "https://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640"
SOURCE_URL = "https://jsd.imki.moe/gh/Kyomotoi/CDN@master/project/ATRI/"

PLUGIN_DIR = Path(".") / "data" / "plugins" / "anti_effort"
PLUGIN_DIR.mkdir(parents=True, exist_ok=True)


class AntiEffort:
    def get_enabled_group(self) -> list:
        groups = list()

        files = os.listdir(PLUGIN_DIR)
        if not files:
            return groups

        for f in files:
            raw_data = f.split(".")
            if raw_data[-1] != "json":
                continue

            if "-ld" in raw_data[0]:
                patt = r"([0-9].*?)-ld"
                match = re.findall(patt, raw_data[0])
                if match:
                    group_id = int(match[0])
                    groups.append(group_id)
            else:
                group_id = int(raw_data[0])
                groups.append(group_id)

        return groups

    def get_data(self, group_id: int) -> dict:
        file_path = PLUGIN_DIR / f"{group_id}.json"
        if not file_path.exists():
            return dict()
        return json.loads(file_path.read_text())

    async def add_user(
        self, group_id: int, user_id: int, user_nickname: str, waka_url: str
    ) -> str:
        patt = (
            r"https:\/\/wakatime.com\/share\/@([a-zA-Z0-9].*?)\/([a-zA-Z0-9].*?).json"
        )
        match = re.findall(patt, waka_url)
        if not match:
            return "哥，你提供的链接有问题啊"

        w_user_id = match[0][1]

        file_path = PLUGIN_DIR / f"{group_id}.json"
        if not file_path.exists():
            now_time = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
            d = AntiEffortModel(update_time=now_time, data=list()).dict()
            with open(file_path, "w") as f:
                f.write(json.dumps(d))

        raw_data = json.loads(file_path.read_text())
        data: list = raw_data["data"]
        for i in data:
            if i["user_id"] == user_id:
                return "你已经在卷王统计榜力！"

        try:
            resp = await request.get(waka_url)
            user_w_data = resp.json()  # type: ignore

            d = user_w_data["data"]
            last_7_days_count = float()
            recent_count = float(d[-1]["grand_total"]["decimal"])
            for u in d:
                last_7_days_count += float(u["grand_total"]["decimal"])
        except Exception:
            log.error(f"获取卷王 {w_user_id} 数据失败！")
            last_7_days_count = int()
            recent_count = int()

        data.append(
            AntiEffortUserModel(
                user_id=user_id,
                user_nickname=user_nickname,
                w_user_id=w_user_id,
                waka_url=waka_url,
                last_7_days_count=last_7_days_count,
                recent_count=recent_count,
            ).dict()
        )
        raw_data["data"] = data
        with open(file_path, "w") as f:
            f.write(json.dumps(raw_data))

        return "成功加入卷王统计榜！"

    def del_user(self, group_id: int, user_id: int) -> str:
        raw_data = self.get_data(group_id)
        if raw_data:
            file_path = PLUGIN_DIR / f"{group_id}.json"
            data = raw_data["data"]
            for i in data:
                if i["user_id"] == user_id:
                    data.remove(i)
                    raw_data["data"] = data
                    with open(file_path, "w") as f:
                        f.write(json.dumps(raw_data))
                    return "成功退出卷王统计榜！"

        return "你未加入卷王统计榜捏"

    def update_user(self, group_id: int, user_id: int, update_map: dict):
        raw_data = self.get_data(group_id)
        if raw_data:
            now_time = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
            file_path = PLUGIN_DIR / f"{group_id}.json"
            data = raw_data["data"]
            for i in data:
                if i["user_id"] == user_id:
                    for k, v in update_map.items():
                        i[k] = v
                    raw_data["update_time"] = now_time
                    raw_data["data"] = data
                    with open(file_path, "w") as f:
                        f.write(json.dumps(raw_data))

    def store_user_data_recent(self):
        groups = self.get_enabled_group()
        if not groups:
            return

        for g in groups:
            data = self.get_data(g)
            if not data:
                return

            file_path = PLUGIN_DIR / f"{g}-ld.json"
            with open(file_path, "w") as f:
                f.write(json.dumps(data))

    async def update_data(self):
        groups = self.get_enabled_group()

        for i in groups:
            raw_data = self.get_data(i)
            if not raw_data:
                continue

            data = raw_data["data"]
            for j in data:
                try:
                    resp = await request.get(j["waka_url"])
                    user_w_data = resp.json()  # type: ignore
                except Exception:
                    log.error(f"获取卷王 {j['user_id']} 数据失败！")
                    continue

                d = user_w_data.get("data", dict())
                if not d:
                    continue

                user_w_last_7_days_count = float()
                user_w_recent_count = float(d[-1]["grand_total"]["decimal"])
                for u in d:
                    user_w_last_7_days_count += float(u["grand_total"]["decimal"])

                u_data = {
                    "last_7_days_count": user_w_last_7_days_count,
                    "recent_count": user_w_recent_count,
                }
                self.update_user(i, j["user_id"], u_data)

    async def gen_img(
        self, user_id: int, user_nickname: str, coding_time: float
    ) -> str:

        try:
            resp = await request.get(TENCENT_AVATER_URL.format(user_id=user_id))
        except Exception:
            log.error("插件 anti_effort 获取用户头像失败！")
            return str()

        avatar_byt = resp.read()  # type: ignore
        result = image_dealer(
            avatar_byt, user_nickname, str(round(coding_time, 2)) + " hrs"
        )
        return f"file:///{result}"

    def gen_rank(self, raw_data: dict, user_id: int, typ: str) -> str:
        table_type = "Today"
        sort_type = "recent_count"
        if typ == "today":
            rank_type = "今日"
        elif typ == "recent_week":
            rank_type = "近一周"
            table_type = "Last 7 Days"
            sort_type = "last_7_days_count"
        elif typ == "global_today":
            rank_type = "今日公共"
        else:
            rank_type = "近一周公共"
            table_type = "Last 7 Days"
            sort_type = "last_7_days_count"

        data = raw_data["data"]
        data = sorted(data, key=lambda x: x[sort_type], reverse=True)

        user_rank = 0
        user_recent_count = 0
        for i, user in enumerate(data):
            if user["user_id"] == user_id:
                user_rank = i + 1
                user_recent_count = user["recent_count"]
                break

        if not user_recent_count:
            user_rank = 0

        table = [
            [
                f"{i + 1}",
                f"{x['user_nickname']}",
                f"{round(x[sort_type], 2)} hrs",
            ]
            for i, x in enumerate(data)
        ][:10]
        table.insert(0, ["Rank", "Member", table_type])
        result = tabulate(table, tablefmt="plain")
        update_time = raw_data["update_time"]
        rank = f"\n你位于第 {user_rank} 名: {user_recent_count} hrs" if user_rank else str()
        repo = f"《{rank_type}十佳卷王》\nUpdate Time: {update_time}\n{result}{rank}"
        return repo


async def init_source():
    files = ["xb-bg-0.png", "hwxw.ttf"]

    try:
        for i in files:
            file_path = PLUGIN_DIR / i
            if not file_path.is_file():
                log.warning("插件 anti_effort 缺少所需资源，装载中")
                url = SOURCE_URL + i
                data = await request.get(url)
                with open(file_path, "wb") as f:
                    f.write(data.read())  # type: ignore
    except Exception:
        ServiceTools.service_controller("谁是卷王", False)
        log.error(f"插件 anti_effort 装载资源失败. 已自动禁用")

    log.success("插件 anti_effort 装载资源完成")


driver().on_startup(init_source)
