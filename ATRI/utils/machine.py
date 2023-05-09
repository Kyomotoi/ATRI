import psutil
import platform
from pydantic import BaseModel
from sys import platform as pf

from .apscheduler import scheduler

if pf == "win32":
    import wmi
    from win32com.client import GetObject


class PlatformInfo(BaseModel):
    name: str
    struct: str
    type: str


class CpuInfo(BaseModel):
    name: str
    count: int
    max_freq: str
    current_freq: str
    percent: float
    process: int


class MemInfo(BaseModel):
    total: int
    available: int
    percent: float
    used: int
    free: int

    swap_total: int
    swap_used: int
    swap_free: int
    swap_percent: float
    swap_sin: int
    swap_sout: int


class DiskInfo(BaseModel):
    name: str
    total: int
    used: int
    free: int
    drive: int
    speed: list[int]


class NetInfo(BaseModel):
    speed: list[int]
    sent_total: int
    recv_total: int
    package_sent: int
    package_recv: int


def get_platform_info() -> PlatformInfo:
    return PlatformInfo(
        name=platform.platform(), struct=platform.architecture()[0], type=pf
    )


def get_cpu_info() -> CpuInfo:
    cpu_name = platform.processor()
    if pf == "win32":
        winm = GetObject("winmgmts:root\cimv2")
        cpus = winm.ExecQuery("SELECT * FROM Win32_Processor")
        cpu_name = cpus[0].Name.strip()

    cpu_count = psutil.cpu_count(False)
    _freq = psutil.cpu_freq()
    cpu_max_freq = f"{'%.2f'%(_freq.max / 1000)}"
    cpu_current_freq = f"{'%.2f'%(_freq.current / 1000)}"
    cpu_percent = psutil.cpu_percent(interval=0.1)
    process = len(psutil.pids())

    return CpuInfo(
        name=cpu_name,
        count=cpu_count,
        max_freq=cpu_max_freq,
        current_freq=cpu_current_freq,
        percent=cpu_percent,
        process=process,
    )


def get_mem_info() -> MemInfo:
    vm = psutil.virtual_memory()
    sm = psutil.swap_memory()
    return MemInfo(
        total=vm.total,
        available=vm.available,
        percent=vm.percent,
        used=vm.used,
        free=vm.free,
        swap_total=sm.total,
        swap_used=sm.used,
        swap_free=sm.free,
        swap_percent=sm.percent,
        swap_sin=sm.sin,
        swap_sout=sm.sout,
    )


last_disk_io = [0, 0]
now_disk_io = [0, 0]


@scheduler.scheduled_job("interval", seconds=1, misfire_grace_time=15)
async def _():
    global last_disk_io, now_disk_io

    disk_counters = psutil.disk_io_counters()
    now_disk_io = [
        disk_counters.write_bytes - last_disk_io[0],  # type: ignore
        disk_counters.read_bytes - last_disk_io[1],  # type: ignore
    ]
    last_disk_io = [disk_counters.write_bytes, disk_counters.read_bytes]  # type: ignore


def get_disk_info():
    disk_name = "ATRI Disk Pro Plus"
    disk_total = int()
    disk_used = int()
    disk_free = int()
    disk_drive = 1
    if pf == "win32":
        w = wmi.WMI()
        disk_list = [d.DeviceID for d in w.Win32_LogicalDisk()]
        for i in disk_list:
            disk = psutil.disk_usage(i)
            disk_total += disk.total
            disk_used += disk.used
            disk_free += disk.free

        disk_name = w.Win32_DiskDrive()[0].Model
        disk_drive = len(w.Win32_DiskDrive())
    else:
        disk = psutil.disk_usage("/")
        disk_total = disk.total
        disk_used = disk.used
        disk_free = disk.free

    return DiskInfo(
        name=disk_name,
        total=disk_total,
        used=disk_used,
        free=disk_free,
        drive=disk_drive,
        speed=now_disk_io,
    )


last_net_io = [0, 0]
now_net_io = [0, 0]


@scheduler.scheduled_job("interval", seconds=1, misfire_grace_time=15)
async def _():
    global last_net_io, now_net_io

    net_counters = psutil.net_io_counters()
    now_net_io = [
        net_counters.bytes_sent - last_net_io[0],
        net_counters.bytes_recv - last_net_io[1],
    ]
    last_net_io = [net_counters.bytes_sent, net_counters.bytes_recv]


def get_net_info():
    net = psutil.net_io_counters()
    return NetInfo(
        speed=now_net_io,
        sent_total=net.bytes_sent,
        recv_total=net.bytes_recv,
        package_sent=net.packets_sent,
        package_recv=net.packets_recv,
    )
