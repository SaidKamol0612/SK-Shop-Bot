from aiogram import Router, F
from aiogram.types import Message, URLInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.db.crud import (
    get_count_products_in_cart,
    is_liked,
)
from app.db.crud import (
    get_products_in_cart,
    remove_product_from_cart,
    activate_order,
    activate_one_order,
)
from app.db import db_helper
from app.keyboard.inline import product_kb, order_kb, one_order_kb
from app.keyboard.reply import main_kb
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
        await message.answer(
            get_i18n_msg("accept_order", lang), reply_markup=order_kb(lang)
        )


@router.callback_query(
    AppState.show_products_in_cart, F.data.startswith("confirm_order")
)
async def accept_order_handler(callback: CallbackQuery, state: FSMContext):
    lang = (await state.get_data()).get("lang")

    # TODO: Implement order activation logic

    async with db_helper.session_factory() as session:
        await activate_order(session, callback.from_user.id)

    await callback.message.answer(
        get_i18n_msg("order_accepted", lang), reply_markup=main_kb(lang)
    )


@router.callback_query(F.data.startswith("buy_now"))
async def accept_order_handler(callback: CallbackQuery, state: FSMContext):
    lang = (await state.get_data()).get("lang")
    product_id = int(callback.data.split(":")[1])

    await state.set_state(AppState.waiting_confirm_order)
    await callback.message.answer(
        get_i18n_msg("ask_confirm_one_order", lang),
        reply_markup=one_order_kb(lang, product_id),
    )


@router.callback_query(
    AppState.waiting_confirm_order, F.data.startswith("confirm_one_order")
)
async def confirm_one_order_handler(callback: CallbackQuery, state: FSMContext):
    lang = (await state.get_data()).get("lang")
    product_id = int(callback.data.split(":")[1])

    async with db_helper.session_factory() as session:
        await activate_one_order(session, callback.from_user.id, product_id)

    await callback.message.answer(
        get_i18n_msg("order_accepted", lang), reply_markup=main_kb(lang)
    )


@router.callback_query(AppState.show_products_in_cart, F.data.startswith("minus_cart"))
async def minus_cart_handler(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split(":")[1])
    lang = (await state.get_data()).get("lang")

    async with db_helper.session_factory() as session:
        product_count = await get_count_products_in_cart(
            session, callback.from_user.id, product_id
        )

        if product_count > 1:
            await remove_product_from_cart(session, callback.from_user.id, product_id)
            product_count -= 1
            await callback.message.edit_caption(
                caption=callback.message.caption.replace(
                    f"{product_count + 1} {get_i18n_msg('pcs', lang)}",
                    f"{product_count} {get_i18n_msg('pcs', lang)}",
                ),
                reply_markup=product_kb(product_id, lang),
            )
        elif product_count == 1:
            await remove_product_from_cart(session, callback.from_user.id, product_id)
            await callback.message.answer(
                get_i18n_msg("product_removed_from_cart", lang)
            )
            await callback.message.delete()

        cart = await get_products_in_cart(session, callback.from_user.id)
        if len(cart) < 1:
            await callback.message.answer(
                get_i18n_msg("no_cart_products", lang), reply_markup=main_kb(lang)
            )


@router.callback_query(AppState.show_products_in_cart, F.data.startswith("add_to_cart"))
async def add_product_to_cart_handler(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split(":")[1])
    lang = (await state.get_data()).get("lang")

    async with db_helper.session_factory() as session:
        await add_product_to_cart_handler(session, callback.from_user.id, product_id)
        await callback.answer(
            get_i18n_msg("product_added_to_cart", lang), show_alert=True
        )
    await callback.message.edit_caption(
        caption=callback.message.caption.replace(
            f"{get_i18n_msg('pcs', lang)}", f"{get_i18n_msg('pcs', lang)}"
        ),
        reply_markup=product_kb(product_id, lang),
    )
