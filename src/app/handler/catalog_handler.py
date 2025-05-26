from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import URLInputFile

from app.util.api import get_products_from_api
from app.keyboard.reply import catalog_kb
from app.util.i18n import get_i18n_msg
from app.util.crud import get_categories_by_products
from app.state.app import AppState

router = Router()


@router.message(F.text.in_(("🔍 Kod yordamida qidirish", "🔍 Искать с помощью кода")))
async def search_by_code(message: Message, state: FSMContext): ...


@router.message(F.text.in_(("🧾 Katalog", "🧾 Каталог")) | F.text.in_(("🔙 Kategoriyalarga qaytish.", "🔙 Вернуться к категориям.")))
async def catalog(message: Message, state: FSMContext):
    lang = (await state.get_data()).get("lang")

    products = await get_products_from_api(lang)
    categories = get_categories_by_products(products)

    await state.set_state(AppState.choose_category)
    await message.answer(
        get_i18n_msg("categories", lang),
        reply_markup=catalog_kb(categories, is_ctg=True, lang=lang),
    )


@router.message(AppState.choose_category, F.text)
async def choose_category(message: Message, state: FSMContext):
    lang = (await state.get_data()).get("lang")

    products = await get_products_from_api(lang)
    categories = (c["name"] for c in get_categories_by_products(products))

    category_name = message.text.strip()

    if category_name in categories:
        category_products = [p for p in products if p["category"] == category_name]
        if category_products:
            await state.set_state(AppState.choose_product)
            await message.answer(
                get_i18n_msg("category_products", lang),
                reply_markup=catalog_kb(category_products, lang=lang),
            )
    else:
        await message.answer(get_i18n_msg("category_not_found", lang))


@router.message(AppState.choose_product, F.text)
async def choose_category(message: Message, state: FSMContext):
    lang = (await state.get_data()).get("lang")

    products = await get_products_from_api(lang)
    product = next(
        (p for p in products if f"{p['name']} {p['id']}" == message.text.strip()), None
    )

    if product:
        # await state.set_state(AppState.product_details)
        await message.answer_photo(
            photo=URLInputFile(
                url=product["images"][0]["filePath"], filename="product_image.jpg"
            ),
            caption=get_i18n_msg("product_details", lang)
            .replace("name", product["name"])
            .replace("price", str(product["price"]))
            .replace("description", product["shortDescription"]),
        )
    else:
        await message.answer(get_i18n_msg("product_not_found", lang))


@router.message(F.text.in_(("❤️ Sevimlilar", "❤️ Любимые", "❤️ Favorites")))
async def favorites(message: Message, state: FSMContext): ...
