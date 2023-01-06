import os
import json
import psutil
from pathlib import Path
from datetime import datetime

from ATRI.exceptions import GetStatusError

from ATRI.utils import FileDealer
from ATRI.service import ServiceTools, SERVICES_DIR

from . import models


def get_process_info() -> dict:
    try:
        platform_cpu = psutil.cpu_percent(interval=1)
        platform_mem = psutil.virtual_memory().percent
        platform_disk = psutil.disk_usage("/").percent
        platform_net_sent = str(psutil.net_io_counters().bytes_sent / 1000000)
        platform_net_recv = str(psutil.net_io_counters().bytes_recv / 1000000)

        process = psutil.Process(os.getpid())
        bot_cpu = str(process.cpu_percent(interval=1))
        bot_mem = str(process.memory_percent(memtype="rss"))

        now_time = datetime.now().timestamp()
        _boot_time = psutil.boot_time()
        _bot_run_time = process.create_time()
        boot_time = str(
            datetime.utcfromtimestamp(now_time).replace(microsecond=0)
            - datetime.utcfromtimestamp(_boot_time).replace(microsecond=0)
        )
        bot_run_time = str(
            datetime.utcfromtimestamp(now_time).replace(microsecond=0)
            - datetime.utcfromtimestamp(_bot_run_time).replace(microsecond=0)
        )
    except Exception:
        raise GetStatusError("获取实例运行信息失败")

    stat_msg = "アトリは、高性能ですから！"
    if platform_cpu > 90:
        stat_msg = "咱感觉有些头晕..."
        if platform_mem > 90:
            stat_msg = "咱感觉有点头晕并且有点累..."
    elif platform_mem > 90:
        stat_msg = "咱感觉有点累..."
    elif platform_disk > 90:
        stat_msg = "咱感觉身体要被塞满了..."

    platform_cpu = str(platform_cpu)
    platform_mem = str(platform_mem)
    platform_disk = str(platform_disk)

    return models.RuntimeInfo(
        status_message=stat_msg,
        platform_info=models.PlatformRuntimeInfo(
            cpu_percent=platform_cpu,
            mem_percent=platform_mem,
            disk_percent=platform_disk,
            net_sent=platform_net_sent,
            net_recv=platform_net_recv,
            boot_time=boot_time,
        ),
        bot_info=models.BotRuntimeInfo(
            cpu_percent=bot_cpu, mem_percent=bot_mem, run_time=bot_run_time
        ),
    ).dict()


def get_service_list() -> dict:
    result = dict()

    files = os.listdir(SERVICES_DIR)
    for file in files:
        # Thank you, MacOS
        if file == ".DS_Store":
            continue

        service_path = SERVICES_DIR / file
        data = models.ServiceInfo.parse_file(service_path)
        result[data.service] = data.dict()

    return result


def edit_service(
    service: str, global_enabled: int, enabled: bool, user_id: str, group_id: str
):
    data = ServiceTools(service).load_service()

    if global_enabled != 2 and global_enabled:
        data.enabled = bool(global_enabled)
    else:
        data.enabled = False
    if user_id or group_id:
        if enabled:
            if user_id not in data.disable_user:
                return {"detail": "用户不存在于禁用名单"}
            else:
                data.disable_user.remove(user_id)

            if group_id not in data.disable_group:
                return {"detail": "群不存在于禁用名单"}
            else:
                data.disable_group.remove(group_id)
        else:
            if user_id not in data.disable_user:
                data.disable_user.append(user_id)
            else:
                return {"detail": "用户已存在于禁用名单"}

            if group_id not in data.disable_group:
                data.disable_group.append(group_id)
            else:
                return {"detail": "群已存在于禁用名单"}

    ServiceTools(service).save_service(data.dict())

    return {"detail": "操作完成~"}


def get_block_list() -> models.BlockInfo:
    file_dir = Path(".") / "data" / "plugins" / "manege"
    path = file_dir / "block_user.json"
    user_data = json.loads(path.read_bytes())

    path = file_dir / "block_group.json"
    group_data = json.loads(path.read_bytes())

    return models.BlockInfo(user=user_data, group=group_data)


async def edit_block_list(enabled: bool, user_id: str, group_id: str):
    data = get_block_list()
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if enabled:
        if user_id:
            if user_id in data.user:
                return {"detail": "用户已存在于黑名单"}
            else:
                data.user[user_id] = now_time
        if group_id:
            if group_id in data.group:
                return {"detail": "群已存在于黑名单"}
            else:
                data.group[group_id] = now_time
    else:
        if user_id:
            if user_id in data.user:
                del data.user[user_id]
            else:
                return {"detail": "用户不存在于黑名单"}
        if group_id:
            if group_id in data.group:
                del data.group[group_id]
            else:
                return {"detail": "群不存在于黑名单"}

    file_dir = Path(".") / "data" / "plugins" / "manege"
    path = file_dir / "block_user.json"
    await FileDealer(path).write(json.dumps(data.user))

    path = file_dir / "block_group.json"
    await FileDealer(path).write(json.dumps(data.group))

    return {"detail": "操作完成~"}
