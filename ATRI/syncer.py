import sys
import asyncio
import inspect
import types
from functools import singledispatch, wraps

from typing import Any, Callable, Generator


PY37 = sys.version_info >= (3, 7)


def _is_awaitable(co: Generator[Any, None, Any]) -> bool:
    if PY37:
        return inspect.isawaitable(co)
    else:
        return (isinstance(co, types.GeneratorType) or
                isinstance(co, asyncio.Future))


@singledispatch
def sync(co: Any) -> Any:
    raise TypeError(f'Called with unsupported argument: {co}')


@sync.register(asyncio.Future)
@sync.register(types.GeneratorType)
def sync_co(co: Generator[Any, None, Any]) -> Any:
    if not _is_awaitable(co):
        raise TypeError(f'Called with unsupported argument: {co}')
    return asyncio.get_event_loop().run_until_complete(co)


@sync.register(types.FunctionType)
@sync.register(types.MethodType) # type: ignore
def sync_fu(f: Callable[..., Any]) -> Callable[..., Any]:
    if not asyncio.iscoroutinefunction(f):
        raise TypeError(f'Called with unsupported argument: {f}')

    @wraps(f)
    def run(*args, **kwargs) -> Any:
        return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))
    return run


if PY37:
    sync.register(types.CoroutineType)(sync_co)
