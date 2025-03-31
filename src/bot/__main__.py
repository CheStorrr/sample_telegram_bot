import asyncio
import logging
from os import environ

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from .containers import Container
from .database import engine, flush_database, session_factory

from .routers import setup_routers 
from .middlewares import (
    SyncEntitiesMiddleware,
    DatabaseMiddleware
)

dp = Dispatcher()


async def main():
    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=environ.get('BOT_TOKEN'))
    await bot.delete_webhook(drop_pending_updates=True) 
    container = Container(bot=bot)
    container.wire(
        modules=[__name__], packages=['.middlewares', '.routers']
    )

    database_middleware = DatabaseMiddleware(
        session_factory=session_factory
    )

    dp.message.middleware(database_middleware)
    dp.callback_query.middleware(database_middleware)
    dp.message.middleware(SyncEntitiesMiddleware())
    dp.callback_query.middleware(SyncEntitiesMiddleware())
    setup_routers(dp=dp)

    await flush_database(engine)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())