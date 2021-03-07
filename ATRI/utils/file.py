import aiofiles
import urllib
from pathlib import Path

from ATRI.exceptions import RequestTimeOut, WriteError

from .request import get_content


async def write_file(path: Path, text, encoding='utf-8') -> None:
    try:
        async with aiofiles.open(path, 'w', encoding=encoding) as target:
            await target.write(text)
    except WriteError:
        raise WriteError("Writing file failed!")


async def open_file(path: Path, method, encoding='utf-8'):
    try:
        async with aiofiles.open(path, 'r', encoding=encoding) as target:
            if method == "read":
                return target.read()
            elif method == "readlines":
                return await target.readlines()
            elif method == "readline":
                return await target.readline()
            else:
                return target.readable()
    except EOFError:
        raise EOFError("File not fond!")
