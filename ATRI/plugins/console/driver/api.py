import os
import json
import time
import psutil
from pathlib import Path
from datetime import datetime

from ATRI.service import ServiceTools, SERVICES_DIR
from ATRI.exceptions import GetStatusError, ReadFileError, WriteFileError
from ..models import PlatformRuntimeInfo, BotRuntimeInfo, ServiceInfo


def get_processing_data() -> tuple:
    try:
        p_cpu = psutil.cpu_percent(interval=1)
        p_mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        inte_send = psutil.net_io_counters().bytes_sent / 1000000  # type: ignore
        inte_recv = psutil.net_io_counters().bytes_recv / 1000000  # type: ignore

        process = psutil.Process(os.getpid())
        b_cpu = process.cpu_percent(interval=1)
        b_mem = process.memory_percent(memtype="rss")

        now = time.time()
        boot = psutil.boot_time()
        b = process.create_time()
        boot_time = str(
            datetime.utcfromtimestamp(now).replace(microsecond=0)
            - datetime.utcfromtimestamp(boot).replace(microsecond=0)
        )
        bot_time = str(
            datetime.utcfromtimestamp(now).replace(microsecond=0)
            - datetime.utcfromtimestamp(b).replace(microsecond=0)
        )
    except GetStatusError:
        raise GetStatusError("Getting runtime failed.")

    if p_cpu > 90:  # type: ignore
        msg = "咱感觉有些头晕..."
        if p_mem > 90:
            msg = "咱感觉有点头晕并且有点累..."
    elif p_mem > 90:
        msg = "咱感觉有点累..."
    elif disk > 90:
        msg = "咱感觉身体要被塞满了..."
    else:
        msg = "アトリは、高性能ですから！"

    return (
        PlatformRuntimeInfo(
            stat_msg=msg,
            cpu_percent=str(p_cpu),
            mem_percent=p_mem,
            disk_percent=str(disk),
            inte_send=str(inte_send),
            inte_recv=str(inte_recv),
            boot_time=boot_time,
        ).dict(),
        BotRuntimeInfo(
            cpu_percent=str(b_cpu), mem_percent=str(b_mem), bot_run_time=bot_time
        ).dict(),
    )


def get_service_list() -> dict:
    result = dict()

    files = os.listdir(SERVICES_DIR)
    for f in files:
        # Thank you, MacOS
        if f == ".DS_Store":
            continue

        serv_path = SERVICES_DIR / f
        data = json.loads(serv_path.read_bytes())

        serv_name = data["service"]
        serv_docs = data["docs"]
        serv_is_enabled = data["enabled"]
        serv_disable_user = data["disable_user"]
        serv_disable_group = data["disable_group"]

        result[serv_name] = ServiceInfo(
            service_name=serv_name,
            service_docs=serv_docs,
            is_enabled=serv_is_enabled,
            disable_user=serv_disable_user,
            disable_group=serv_disable_group,
        ).dict()

    return result


def control_service(
    serv_name: str, is_enab: int, enab_u: str, enab_g: str, disab_u: str, disab_g: str
) -> tuple:
    try:
        serv_data = ServiceTools().load_service(serv_name)
    except ReadFileError:
        return False, dict()

    if is_enab != 1:
        if is_enab == 0:
            serv_data["enabled"] = False
        else:
            serv_data["enabled"] = True

    if enab_u:
        if enab_u not in serv_data["disable_user"]:
            return False, {"msg": "Target not in list"}
        serv_data["disable_user"].remove(enab_u)

    if enab_g:
        if enab_g not in serv_data["disable_user"]:
            return False, {"msg": "Target not in list"}
        serv_data["disable_group"].remove(enab_g)

    if disab_u:
        if disab_u in serv_data["disable_user"]:
            return False, {"msg": "Target already exists in list"}
        serv_data["disable_user"].append(disab_u)

    if disab_g:
        if disab_g in serv_data["disable_user"]:
            return False, {"msg": "Target already exists in list"}
        serv_data["disable_group"].append(disab_g)

    try:
        ServiceTools().save_service(serv_data, serv_name)
    except WriteFileError:
        return False, dict()

    return True, serv_data


MANEGE_DIR = Path(".") / "data" / "database" / "manege"


def get_block_list() -> dict:
    u_f = "block_user.json"
    path = MANEGE_DIR / u_f
    u_data = json.loads(path.read_bytes())

    g_f = "block_group.json"
    path = MANEGE_DIR / g_f
    g_data = json.loads(path.read_bytes())

    return {"user": u_data, "group": g_data}


def edit_block_list(is_enab: int, user_id: str, group_id: str) -> tuple:
    d = get_block_list()
    u_d = d["user"]
    g_d = d["group"]

    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if is_enab:
        if user_id:
            if user_id in u_d:
                return False, {"msg": "Target already exists in list"}
            u_d[user_id] = now_time

        if group_id:
            if group_id in g_d:
                return False, {"msg": "Target already exists in list"}
            g_d[group_id] = now_time
    else:
        if user_id:
            if user_id not in u_d:
                return False, {"msg": "Target not in list"}
            del u_d[user_id]

        if group_id:
            if group_id not in g_d:
                return False, {"msg": "Target not in list"}
            del g_d[group_id]

    try:
        u_f = "block_user.json"
        path = MANEGE_DIR / u_f
        with open(path, "w", encoding="utf-8") as w:
            w.write(json.dumps(u_d))

        g_f = "block_group.json"
        path = MANEGE_DIR / g_f
        with open(path, "w", encoding="utf-8") as w:
            w.write(json.dumps(g_d))
    except WriteFileError:
        return False, dict()

    return True, {"user": u_d, "group": g_d}
