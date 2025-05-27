from aiogram import Router, F
from aiogram.types import Message, URLInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.db.crud import (
    get_count_products_in_cart,
    is_liked,
)
from app.db.crud.cart import get_products_in_cart
from app.db import db_helper
from app.keyboard.inline import product_kb
from app.util.i18n import get_i18n_msg
from app.state.app import AppState
from app.util.api import get_products_from_api

router = Router()


@router.message(F.text.in_(("🛒 Savat", "🛒 Корзина")))
async def products_in_cart(message: Message, state: FSMContext):
    lang = (await state.get_data()).get("lang")

    async with db_helper.session_factory() as session:
        cart_product = await get_products_in_cart(session, message.from_user.id)

    if not cart_product:
        await message.answer(get_i18n_msg("no_cart_products", lang))
        return
    await state.set_state(AppState.show_products_in_cart)

    all_products = await get_products_from_api(lang)
    cart_product = [p for p in all_products if p["id"] in cart_product]

    for product in cart_product:
        async with db_helper.session_factory() as session:
            liked_unliked = (
                "❤️\n\n"
                if await is_liked(session, message.from_user.id, product["id"])
                else ""
            )

            product_count = await get_count_products_in_cart(
                session, message.from_user.id, product["id"]
            )

        await message.answer_photo(
            photo=URLInputFile(
                url=product["images"][0]["filePath"], filename="product_image.jpg"
            ),
            caption=liked_unliked
            + get_i18n_msg("product_details", lang)
            .replace("name", product["name"])
            .replace("price", str(product["price"]))
            .replace("description", product["shortDescription"])
            .replace("count", f"{product_count}"),
            reply_markup=product_kb(product["id"], lang),
        )
