import nonebot as nb
from pathlib import Path


_sub_plugins = set()

_sub_plugins |= nb.load_plugins(
    str((Path(__file__).parent / 'modules').resolve())) 
