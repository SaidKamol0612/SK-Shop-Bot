from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.state.app import AppState
from app.util.i18n import get_i18n_msg
from app.keyboard.reply import menu_kb, LANG_KB
from app.db.crud import set_user
from app.db import db_helper
from app.util.temp_msg import add_temp_msg, clear_temp_msgs

router = Router()


@router.message(AppState.waiting_for_phone_number, F.contact)
async def main_menu(message: Message, state: FSMContext):
    user_phone_num = message.contact.phone_number
    name = (await state.get_data()).get("name")
    async with db_helper.session_factory() as session:
        await set_user(
            session,
            tg_id=message.from_user.id,
            name=name,
            phone_num=user_phone_num,
        )

    lang = (await state.get_data()).get("lang")

    accept = get_i18n_msg("accept_phone", lang)
    w = get_i18n_msg("welcome_menu", lang)

    await state.set_state(AppState.main)
    await message.answer(f"{accept}\n{w}", reply_markup=menu_kb(lang))


@router.message(
    F.text.in_(("🏠 Bosh menyuga qaytish.", "🏠 Вернуться в главоному меню."))
)
async def back_to_main_menu(message: Message, state: FSMContext):
    await message.delete()
    await clear_temp_msgs(message.from_user.id)

    lang = (await state.get_data()).get("lang")

    await state.set_state(AppState.main)
    await message.answer(
        get_i18n_msg("welcome_menu", lang),
        reply_markup=menu_kb(lang),
    )


@router.callback_query(F.data == "back_to_menu")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Home")
    await callback.message.delete()
    await clear_temp_msgs(callback.from_user.id)

    lang = (await state.get_data()).get("lang")

    await state.set_state(AppState.main)
    await callback.message.answer(
        get_i18n_msg("welcome_menu", lang),
        reply_markup=menu_kb(lang),
    )
