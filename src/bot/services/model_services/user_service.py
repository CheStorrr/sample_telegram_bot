from .. import Service 
from ...models import User
from ...repositories import UserRepository
from typing import Union, Optional

import html


class UserService(Service):

    data: User | None

    def __init__(
        self,
        user_repository: UserRepository
    ):
        super().__init__()
        self.user_repository = user_repository
        self.data = None

    async def get_data(
        self,
        search_argument: Union[str, int]
    ) -> Optional[User]:
        user = None
        if isinstance(search_argument, str):
            user = await self.user_repository.select(username=search_argument)
    
        if search_argument >= 777000:
            user =  await self.user_repository.select(telegram_id=search_argument)
        
        else:
            user = await self.user_repository.select(id=search_argument)

        self.data = user 

        return user
        
    async def update_role(
        self,
        new_role: int
    ):
        if not self.data:
            raise AttributeError(
                f'Data of user for update a role not found'
            )
        if self.data.role_str == new_role:
            return True 
        
        self.data = await self.user_repository.update_role(
            user_id=self.data.id,
            new_role=new_role
        )

        if not self.data: 
            return False 
        
        return True
    
    async def plus_balance(
        self,
        count: int 
    ):
        self.logger.log(f"Запрос на увеличение баланса для [name: {self.data.first_name}; telegram_id: {self.data.telegram_id}; last_chestons: {self.data.chestons}; count: {count}]")


        self.data = await self.user_repository.set_balance(
            count=self.data.chestons+count,
            user_id=self.data.id
        )

    async def minus_balance(
        self,
        count: int 
    ) -> None:
        self.logger.log(f"Запрос на уменьшение баланса для [name: {self.data.first_name}; telegram_id: {self.data.telegram_id}; last_chestons: {self.data.chestons}; count: {count}]")

        self.data = await self.user_repository.set_balance(
            count=self.data.chestons-count,
            user_id=self.data.id
        )

    def create_link(
        self,
        name: str,
        id: Optional[int] = None,
        username: Optional[str] = None
    ) -> str:
        
        name = name.replace('>', '').replace('<', '')
        print(f"name: {name}; id: {id}; username: {username}")
        if id:
            return f"<a href='tg://user?id={id}'>{name}</a>"
        
        elif username:
            return f"<a href='https://t.me/{html.escape(username)}'>{name}</a>"
        
        else:
            return name

