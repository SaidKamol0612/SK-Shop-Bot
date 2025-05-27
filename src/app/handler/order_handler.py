from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.db.crud import get_user_orders, get_products_in_order
from app.db import db_helper
from app.util.i18n import get_i18n_msg
from app.util.api import get_products_from_api
from app.keyboard.reply import main_kb

router = Router()

@router.message(F.text.in_(("📦 Mening buyurtmalarim", "📦 Мои заказы")))
async def my_orders(message: Message, state: FSMContext):
    lang = (await state.get_data()).get("lang")

    async with db_helper.session_factory() as session:
        orders = await get_user_orders(session, message.from_user.id)

    if not orders:
        await message.answer(get_i18n_msg("no_orders", lang))
        return

    response = get_i18n_msg("your_orders", lang)
    
    async with db_helper.session_factory() as session:
        for order in orders:
            products_id = await get_products_in_order(session, order.id)
            products = [p for p in (await get_products_from_api(lang)) if p["id"] in products_id]
            for product in products:
                response += f"\n{product['name']} - {product['price']}\n"
                response += get_i18n_msg("date", lang)
                response += f"{order.created_at}\n"
            
    await message.answer(response, reply_markup=main_kb(lang))