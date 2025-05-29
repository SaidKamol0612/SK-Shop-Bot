from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Cart, ProductCart
from .user import get_user


async def get_cart(session: AsyncSession, user_tg_id: int):
    user_id = (await get_user(session, user_tg_id)).id

    stmt = select(Cart).where(Cart.user_id == user_id, Cart.is_ordered == False)
    cart = await session.scalar(stmt)

    if not cart:
        cart = Cart(user_id=user_id, is_ordered=False)
        session.add(cart)
        await session.commit()
        await session.refresh(cart)

    return cart


async def remove_product_from_cart(
    session: AsyncSession, user_tg_id: int, product_id: int
):
    cart = await get_cart(session, user_tg_id)

    stmt = select(ProductCart).where(
        ProductCart.cart_id == cart.id, ProductCart.product_id == product_id
    )
    product_cart = await session.scalar(stmt)

    if product_cart:
        product_cart.product_count -= 1

        if product_cart.product_count <= 0:
            await session.delete(product_cart)
            await session.commit()
            return
        await session.commit()
        await session.refresh(product_cart)


async def add_product_to_cart(session: AsyncSession, user_tg_id: int, product_id: int):
    cart = await get_cart(session, user_tg_id)

    stmt = select(ProductCart).where(
        ProductCart.cart_id == cart.id, ProductCart.product_id == product_id
    )
    product_cart = await session.scalar(stmt)

    if product_cart:
        product_cart.product_count += 1
        await session.commit()
        await session.refresh(product_cart)
    else:
        product_cart = ProductCart(
            cart_id=cart.id, product_id=product_id, product_count=1
        )
        session.add(product_cart)
        await session.commit()
        await session.refresh(product_cart)


async def get_count_products_in_cart(
    session: AsyncSession, user_tg_id: int, product_id: int
):
    cart = await get_cart(session, user_tg_id)

    stmt = select(ProductCart).where(
        ProductCart.cart_id == cart.id, ProductCart.product_id == product_id
    )
    product_cart = await session.scalar(stmt)

    return product_cart.product_count if product_cart else 0


async def get_products_in_cart(session: AsyncSession, user_tg_id: int):
    cart = await get_cart(session, user_tg_id)

    stmt = select(ProductCart).where(ProductCart.cart_id == cart.id)
    product_carts = await session.scalars(stmt)

    return [product.product_id for product in product_carts]


async def activate_order(session: AsyncSession, user_tg_id: int):
    cart = await get_cart(session, user_tg_id)
    cart.is_ordered = True
    await session.commit()
    await session.refresh(cart)


async def activate_one_order(session: AsyncSession, user_tg_id: int, product_id: int):
    cart = Cart(
        user_id=(await get_user(session, user_tg_id)).id,
        is_ordered=True,
    )
    session.add(cart)
    await session.commit()
    await session.refresh(cart)

    product_cart = ProductCart(
        cart_id=cart.id,
        product_id=product_id,
        product_count=1,
    )
    session.add(product_cart)
    await session.commit()
    await session.refresh(product_cart)

async def get_user_orders(session: AsyncSession, user_tg_id: int):
    user_id = (await get_user(session, user_tg_id)).id

    stmt = select(Cart).where(Cart.user_id == user_id, Cart.is_ordered == True)
    orders = await session.scalars(stmt)

    return [order for order in orders]

async def get_products_in_order(session: AsyncSession, order_id: int):
    stmt = select(ProductCart).where(
        ProductCart.cart_id == order_id
    )
    product_carts = await session.scalars(stmt)

    return [product.product_id for product in product_carts]