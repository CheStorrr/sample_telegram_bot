from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from ..exceptions import RecordNotFoundError
from ..models import Chat
from . import Repository


class ChatRepository(Repository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert(
        self,
        telegram_id: int,
        title: str,
        username: Optional[str] = None,
    ):
        return await self.session.scalar(
            insert(Chat)
            .values(
                telegram_id=telegram_id,
                title=title,
                username=username
            )
            .on_conflict_do_update(
                index_elements=['telegram_id'],
                set_={
                    'title': title,
                    'username': username,
                },
            )
            .returning(Chat)
        )

    async def find_by_telegram_id(self, telegram_id: int) -> Optional[Chat]:
        group = await self.session.scalar(
            select(Chat).filter(Chat.telegram_id == telegram_id).limit(1)
        )

        if group is None:
            raise RecordNotFoundError(
                f'Group with telegram_id={telegram_id} not found'
            )

        return group
