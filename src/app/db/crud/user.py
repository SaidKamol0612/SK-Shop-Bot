from sqlalchemy import select, BigInteger

from app.db import db_helper
from app.db.models import User


async def is_registered_user(user_id: str) -> bool:
    async with db_helper.session_factory() as session:
        stmt = select(User).where(User.tg_id == user_id)
        res = await session.scalar(stmt)

        return res is not None


async def set_user(tg_id: BigInteger, name: str, phone_num: str):
    async with db_helper.session_factory() as session:
        new_user = User(tg_id=tg_id, name=name, phone_num=phone_num)

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
