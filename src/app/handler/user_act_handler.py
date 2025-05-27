from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.db.crud import get_user
from app.db import db_helper
from app.util.i18n import get_i18n_msg

router = Router()


@router.message(F.text.in_(("🗂 Ma'lumotlarim", "🗂 Мои информации", "🗂 My info")))
async def my_info(message: Message, state: FSMContext):
    async with db_helper.session_factory() as session:
        current = await get_user(session, message.from_user.id)
    lang = (await state.get_data()).get("lang")

    info = get_i18n_msg("user_info", lang)
    await message.answer(
        (f"<b>{info[0]}</b>: {current.name}\n" f"<b>{info[1]}</b>: {current.phone_num}")
    )


@router.message(
    F.text.in_(("📦 Mening buyurtmalarim", "📦 Мои заказы", "📦 My orders"))
)
async def my_orders(message: Message, state: FSMContext): ...
