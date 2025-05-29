from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .user import get_user
from app.db.models import Favorite


async def like_unlike_product(session: AsyncSession, user_tg_id: int, product_id: int):
    user_id = (await get_user(session, user_tg_id)).id

    stmt = select(Favorite).where(
        Favorite.user_id == user_id, Favorite.product_id == product_id
    )
    favorite = await session.scalar(stmt)

    if favorite:
        await session.delete(favorite)
        await session.commit()
        return False
    else:
        new_favorite = Favorite(user_id=user_id, product_id=product_id)
        session.add(new_favorite)
        await session.commit()
        await session.refresh(new_favorite)
        return True


async def is_liked(session: AsyncSession, user_tg_id: int, product_id: int):
    user_id = (await get_user(session, user_tg_id)).id

    stmt = select(Favorite).where(
        Favorite.user_id == user_id, Favorite.product_id == product_id
    )
    favorite = await session.scalar(stmt)

    return favorite is not None


async def get_favorites(session: AsyncSession, user_tg_id: int):
    user_id = (await get_user(session, user_tg_id)).id

    stmt = select(Favorite).where(Favorite.user_id == user_id)
    favorites = await session.scalars(stmt)

    return [fav.product_id for fav in favorites]
