from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from dependency_injector.wiring import Provide

from ..containers import Container
from ..services import SyncEntitiesService
from ..repositories import UserRepository, ChatRepository


class SyncEntitiesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
        sync_entities_service: SyncEntitiesService = Provide[
            Container.sync_entities_services
        ]
    ) -> Any:
        
        await sync_entities_service(event=event)
        
        return await handler(event, data)   