import nonebot
from pathlib import Path


_sub_plugins = set()

_sub_plugins |= nonebot.load_plugins(str((Path(__file__).parent / "modules").resolve()))
