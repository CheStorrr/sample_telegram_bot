from aiogram import Router, F
from aiogram.types import Message 



router = Router(name=__name__)

@router.message(F.text)
async def all_messages_handler(
    message: Message
):
    
    pass