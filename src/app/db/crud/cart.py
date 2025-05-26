from sqlalchemy import select

from app.db.models import User, Cart, ProductCart, Favorite
from app.db import db_helper
from .user import get_user


async def get_cart(user_tg_id: int):
    async with db_helper.session_factory() as session:
        user_id = (await get_user(user_tg_id)).id

        stmt = select(Cart).where(Cart.user_id == user_id, Cart.is_ordered == False)
        cart = await session.scalar(stmt)

        if not cart:
            cart = Cart(user_id=user_id, is_ordered=False)
            session.add(cart)
            await session.commit()
            await session.refresh(cart)

        return cart


async def add_product_to_cart(user_tg_id: int, product_id: int):
    async with db_helper.session_factory() as session:
        cart = await get_cart(user_tg_id)

        stmt = select(ProductCart).where(
            ProductCart.cart_id == cart.id, ProductCart.product_id == product_id
        )
        product_cart = await session.scalar(stmt)

        if product_cart:
            product_cart.product_count += 1
        else:
            product_cart = ProductCart(
                cart_id=cart.id, product_id=product_id, product_count=1
            )
            session.add(product_cart)
        await session.commit()
        await session.refresh(product_cart)


async def get_count_products_in_cart(user_tg_id: int, product_id: int):
    async with db_helper.session_factory() as session:
        cart = await get_cart(user_tg_id)

        stmt = select(ProductCart).where(
            ProductCart.cart_id == cart.id, ProductCart.product_id == product_id
        )
        product_cart = await session.scalar(stmt)

        if product_cart:
            return product_cart.product_count
        return 0


async def like_unlike_product(user_tg_id: int, product_id: int):
    async with db_helper.session_factory() as session:
        user_id = (await get_user(user_tg_id)).id

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
