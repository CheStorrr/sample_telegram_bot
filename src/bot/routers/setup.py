from aiogram import Dispatcher 

from . import (
    StartRouterDeepLinkFalse,
    AllMessagesRouter,
)

from ..middlewares import AdminMiddleware

def setup_routers(dp: Dispatcher):


    dp.include_routers(
        StartRouterDeepLinkFalse,
    )

    dp.include_router(AllMessagesRouter)