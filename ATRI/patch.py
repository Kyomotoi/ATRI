from typing import Optional
from contextlib import AsyncExitStack

from nonebot.log import logger
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State, T_DependencyCache
from nonebot.matcher import (
    Matcher,
    current_bot,
    current_event,
    current_handler,
    current_matcher,
)
from nonebot.exception import SkippedException, StopPropagation


async def simple_run(
    self: Matcher,
    bot: Bot,
    event: Event,
    state: T_State,
    stack: Optional[AsyncExitStack] = None,
    dependency_cache: Optional[T_DependencyCache] = None,
):
    logger.debug(
        f"{self} run with incoming args: "
        f"bot={bot}, event={event!r}, state={state!r}"
    )
    b_t = current_bot.set(bot)
    e_t = current_event.set(event)
    m_t = current_matcher.set(self)
    try:
        # Refresh preprocess state
        self.state.update(state)

        while self.handlers:
            handler = self.handlers.pop(0)
            current_handler.set(handler)
            logger.debug(f"Running handler {handler}")
            try:
                await handler(
                    matcher=self,
                    bot=bot,
                    event=event,
                    state=self.state,
                    stack=stack,
                    dependency_cache=dependency_cache,
                )
            except SkippedException:
                logger.debug(f"Handler {handler} skipped")
    except StopPropagation:
        self.block = True
    finally:
        logger.debug(f"{self} running complete")
        current_bot.reset(b_t)
        current_event.reset(e_t)
        current_matcher.reset(m_t)


Matcher.simple_run = simple_run
