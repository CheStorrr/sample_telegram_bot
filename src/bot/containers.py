from contextvars import ContextVar

from aiogram import Bot
from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession

from .services import (
    SyncEntitiesService,
    UserService,
)
from .repositories import (
    UserRepository,
    ChatRepository,
)


session_context: ContextVar[AsyncSession] = ContextVar('session_context')


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    bot = providers.Dependency(instance_of=Bot)

    db_session = providers.Factory(lambda: session_context.get())

    user_repository: UserRepository = providers.Factory(
        UserRepository, session=db_session
    )
    chat_repository: ChatRepository = providers.Factory(
        ChatRepository, session=db_session
    )
    
    
    sync_entities_services: SyncEntitiesService = providers.Factory(
        SyncEntitiesService, user_repository, chat_repository
    )

    user_service: UserService = providers.Factory(
        UserService, user_repository
    )

   
