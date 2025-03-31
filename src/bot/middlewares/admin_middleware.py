from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from ..config import Config


class AdminMiddleware(BaseMiddleware):

    def __init__(self, *args):
        return super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        if isinstance(event, Message) or isinstance(event, CallbackQuery):
            if event.from_user.id not in Config.bot_admins:
                return None

            return await handler(event, data)
        
        return None