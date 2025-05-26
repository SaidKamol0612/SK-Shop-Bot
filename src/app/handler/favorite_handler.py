from aiogram import Router, F
from aiogram.types import Message, URLInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.db.crud import get_favorites, get_count_products_in_cart
from app.db.crud import is_liked, like_unlike_product
from app.keyboard.inline import product_kb
from app.util.i18n import get_i18n_msg
from app.state.app import AppState
from app.util.api import get_products_from_api

router = Router()


@router.message(F.text.in_(("❤️ Sevimlilar", "❤️ Любимые")))
async def favorites(message: Message, state: FSMContext):
    lang = (await state.get_data()).get("lang")

    favorites = await get_favorites(message.from_user.id)

    if not favorites:
        await message.answer(get_i18n_msg("no_favorites", lang))
        return
    await state.set_state(AppState.show_favorites)

    all_products = await get_products_from_api(lang)
    favorites = [p for p in all_products if p["id"] in favorites]

    for product in favorites:
        liked_unliked = (
            "❤️\n\n" if await is_liked(message.from_user.id, product["id"]) else ""
        )

        product_count = await get_count_products_in_cart(
            message.from_user.id, product["id"]
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


@router.callback_query(
    AppState.show_favorites, F.data.startswith("like_unlike")
)
async def like_unlike(callback: CallbackQuery, state: FSMContext):
    lang = (await state.get_data()).get("lang")
    product_id = int(callback.data.split(":")[1])

    res = await like_unlike_product(callback.from_user.id, product_id)
    
    if res:
        await callback.answer(get_i18n_msg("liked_unliked", lang)[0], show_alert=True)
    else:
        await callback.answer(get_i18n_msg("liked_unliked", lang)[1], show_alert=True)
    await callback.message.delete()


    favorites = await get_favorites(callback.from_user.id)

    if not favorites:
        await callback.message.answer(get_i18n_msg("no_favorites", lang))
        return
