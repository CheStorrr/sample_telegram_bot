from ..repositories import (
    UserRepository,
    ChatRepository,
)
from . import Service 
from aiogram.types import TelegramObject, Message, CallbackQuery, InlineQuery


class SyncEntitiesService(Service):

    def __init__(
        self,
        user_repository: UserRepository,
        chat_repository: ChatRepository
    ):
        super().__init__()
        self.user_repository: UserRepository = user_repository
        self.chat_repository: ChatRepository = chat_repository

    async def __call__(
        self,
        event: TelegramObject
    ) -> None:
        
        await self.user_repository.upsert(
            telegram_id=event.from_user.id,
            first_name=event.from_user.first_name,
            last_name=event.from_user.last_name,
            username=event.from_user.username
        )

        

        if isinstance(event, InlineQuery) and event.chat_type != "private":
            return None
        
        elif isinstance(event, CallbackQuery) and event.message.chat.type != "private":
            await self.chat_repository.upsert(
                telegram_id=event.message.chat.id,
                title=event.message.chat.title,
                username=event.message.chat.username
            )

        elif isinstance(event, Message) and event.chat.type != "private":
            await self.chat_repository.upsert(
                telegram_id=event.chat.id,
                title=event.chat.title,
                username=event.chat.username
            )

        