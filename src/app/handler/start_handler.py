from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.state.app import AppState
from app.db.crud import is_registered_user
from app.db import db_helper
from app.util.i18n import get_i18n_msg
from app.keyboard.reply import send_phone_kb, menu_kb

router = Router()


@router.message(AppState.choose_lang, F.text)
async def uzbek_language_handler(message: Message, state: FSMContext):
    msg = message.text
    if msg == ("🇺🇿 O'zbekcha"):
        await state.update_data(lang="uz")
        await message.answer("🇺🇿 Siz o'zbek tilini tanladingiz.")
    elif msg == ("🇷🇺 Русский"):
        await state.update_data(lang="ru")
        await message.answer("🇷🇺 Вы выбрали русский язык.")
    else:
        await message.answer(
            "⚠️ Iltimos to'gri tilni tanlang.\n⚠️ Пожалуйста выберите правильный язык."
        )
        return

    async with db_helper.session_factory() as session:
        is_user = await is_registered_user(session, message.from_user.id)

    if is_user:
        lang = (await state.get_data()).get("lang")
        w = get_i18n_msg("welcome_menu", lang)
        await state.set_state(AppState.main)
        await message.answer(w, reply_markup=menu_kb(lang))
    else:
        lang = (await state.get_data()).get("lang")
        await state.set_state(AppState.waiting_for_phone_number)
        await message.answer(
            get_i18n_msg("request_phone", lang), reply_markup=send_phone_kb(lang)
        )
