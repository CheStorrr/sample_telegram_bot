from aiogram.filters import Filter 
from aiogram.types import Message
from typing import Optional


class Text(Filter):

    def __init__(
        self,
        text: str,
        lower: bool = True,
        split: Optional[int] = None,
        in_ : bool = False
    ):
        self.text = text
        self.lower = lower
        self.split = split
        self.in_ = in_

    async def __call__(
        self, 
        message: Message
    ) -> bool:
        if not message.text:
            return False
        
        text = message.text
        
        if self.lower:
            text = text.lower()

        if self.split:
            text = text.split()[self.split]

        if self.in_: 
            if self.text in text:
                return True 
            return False

        if text == self.text:
            return True 

        return False