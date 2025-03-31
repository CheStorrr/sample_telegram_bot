from aiogram.filters import Filter 
from aiogram.types import CallbackQuery
from typing import Optional


class CallData(Filter):

    def __init__(
        self,
        data: str,
        lower: bool = True,
        split: Optional[int] = None,
        in_: bool = False
    ):
        self.data = data
        self.in_ = in_
        self.lower = lower

        self.split = split

    async def __call__(
        self, 
        call: CallbackQuery
    ) -> bool:
        if not call.data:
            return False
        
        data = call.data
        
        if self.lower:
            data = data.lower()

        if self.split:
            data = data.split()[self.split]

        if self.in_:
            if self.data in data:
                return True 
            return False
        
        if data == self.data:
            return True 
        
        
        return False