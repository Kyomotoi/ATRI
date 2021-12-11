from ATRI.config import ChatterBot
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from ATRI.log import logger as log

__doc__ = """
可以不断学习的聊天(胡言乱语/复读)机器人
https://chatterbot.readthedocs.io/
"""

MONGO_ADAPTER = "chatterbot.storage.MongoDatabaseAdapter"
SQLITE_ADAPTER = "chatterbot.storage.SQLStorageAdapter"

class ATRIChatBot:
    bot = ChatBot(
        "ATRI",
        storage_adapter=MONGO_ADAPTER if ChatterBot.mongo_database_uri else SQLITE_ADAPTER,
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': ChatterBot.default_response,
                'maximum_similarity_threshold': ChatterBot.maximum_similarity_threshold
            }
        ],
        database_uri=ChatterBot.mongo_database_uri,
        read_only=True  # 只能通过 learn 函数学习
    )
    list_trainer = ListTrainer(bot)
    session_text_dict = dict()

    @staticmethod
    def learn_from_corpus():
        trainer = ChatterBotCorpusTrainer(ATRIChatBot.bot)
        # 从 corpus 的中文语料库学习,yaml 包太新的话需要把 corpus.py 的 yaml.load() 改成 yaml.full_load()
        # 可以尝试用 https://github.com/hbwzhsh/chinese_chatbot_corpus 里面的语料进行训练
        trainer.train("chatterbot.corpus.chinese")

    @staticmethod
    def learn(session_id: str, text: str):
        # 查找上一条消息并训练模型
        last_text = ATRIChatBot.session_text_dict.get(session_id)
        if last_text:
            ATRIChatBot.list_trainer.train([
                last_text,  # 问(可多个)
                text  # 答
            ])
        # 更新最后一条消息
        ATRIChatBot.session_text_dict[session_id] = text

    @staticmethod
    async def get_response(text: str) -> str:
        response = ATRIChatBot.bot.get_response(text)
        log.info(f"人工智障回复:{text}  ->  {response.text}")
        return response.text