import asyncio
from functools import partial
from typing import Any


async def run_sync_func(func, *args, **kwargs) -> Any:
    return await asyncio.get_event_loop().run_in_executor(
        None, partial(func, *args, **kwargs))
