
from typing import Optional

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from ..exceptions import RecordNotFoundError, SelectError
from ..models import User
from . import Repository


class UserRepository(Repository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert(
        self,
        telegram_id: int,
        first_name: str,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
    ) -> User:
        user = await self.session.scalar(
            insert(User)
            .values(
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
            )
            .on_conflict_do_update(
                index_elements=['telegram_id'],
                set_={
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': username,
                },
            )
            .returning(User)
        )

        if user is None:
            raise RecordNotFoundError(
                f'User with telegram_id={telegram_id} not found'
            )

        return user
    
    async def select(
        self,
        telegram_id: Optional[int] = None,
        id: Optional[int] = None,
        username: Optional[str] = None
    ) -> Optional[User]:
        
        query = select(User)

        if telegram_id:
            query = query.where(User.telegram_id == telegram_id)

        elif id:
            query = query.where(User.id == id)

        elif username:
            query = query.where(User.username == username)

        else: 
            raise SelectError('Не был передан ни один аргумент')
        
        return await self.session.scalar(query)
    
 