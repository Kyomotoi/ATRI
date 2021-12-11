import random
from ATRI.config import ChatterBot
from ATRI.plugins.atri_chat_bot import ATRIChatBot
from nonebot import on_message
from nonebot import on_command
from nonebot.adapters.cqhttp import (
    Bot,
    GroupMessageEvent,
    MessageEvent,
)
from nonebot.permission import SUPERUSER

chatbot = on_message(priority=114514)


@chatbot.handle()
async def _learn_from_group(bot: Bot, event: MessageEvent):
    text = event.get_plaintext().strip()
    if not text:
        return
    if isinstance(event, GroupMessageEvent):  # 从群友那学习说话
        ATRIChatBot.learn(event.get_session_id(), text)
        if random.random() <= ChatterBot.group_random_response_rate:  # 随机回话
            await chatbot.finish(await ATRIChatBot.get_response(text))


chatbot_learn = on_command("/learn_corpus", permission=SUPERUSER)


@chatbot_learn.handle()
async def _learn_from_corpus(bot: Bot, event: MessageEvent):
    ATRIChatBot.learn_from_corpus()
    await chatbot.finish("咱从corpus那学习完了!")
