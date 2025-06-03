from sqlalchemy import select, BigInteger
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


async def is_registered_user(session: AsyncSession, user_id: str) -> bool:
    stmt = select(User).where(User.tg_id == user_id)
    res = await session.scalar(stmt)

    return res is not None


async def set_user(
    session: AsyncSession, tg_id: BigInteger, name: str, phone_num: str
) -> None:
    new_user = User(tg_id=tg_id, name=name, phone_num=phone_num)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)


async def get_user(session: AsyncSession, tg_id: BigInteger) -> User:
    stmt = select(User).where(User.tg_id == tg_id)
    res = await session.scalar(stmt)

    return res

async def get_users(session: AsyncSession):
    stmt = select(User)
    res = await session.scalars(stmt)
    
    return [u for u in res]