from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ai_bot.core.database.models import Users


async def put_access_token_db(session: AsyncSession, data: dict):
    obj = Users(
        user_id=data["user_id"],
        access_token=data["access_token"]
    )
    session.add(obj)
    await session.commit()


async def get_access_token_db(session: AsyncSession, data: dict):
    query = select(Users).where(Users.user_id == data["user_id"])

    result = await session.execute(query)
    return result.scalars().all()

async def get_all_users_db(session: AsyncSession):
    query = select(Users)

    result = await session.execute(query)
    return result.scalars().all()