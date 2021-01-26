from nonebot.adapters.cqhttp import Bot


class Send:
    @staticmethod
    async def send_to_superuser(message: str) -> None:
        from ATRI.config import RUNTIME_CONFIG
        async def _send_to_superuser(bot: Bot) -> None:
            for sup in RUNTIME_CONFIG['superusers']:
                await bot.send_private_msg(
                    user_id=sup,
                    message=message
                )
