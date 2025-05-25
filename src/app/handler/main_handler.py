from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.state.registraion import RegistrationStates
from app.state.app import AppState
from app.util.i18n import get_i18n_msg
from app.keyboard.reply import menu_kb, LANG_KB
from app.db.crud import set_user

router = Router()


@router.message(RegistrationStates.waiting_for_phone_number, F.contact)
async def main_menu(message: Message, state: FSMContext):
    user_phone_num = message.contact.phone_number

    await set_user(
        tg_id=message.from_user.id,
        name=message.from_user.first_name,
        phone_num=user_phone_num,
    )

    lang = (await state.get_data()).get("lang")

    accept = get_i18n_msg("accept_phone", lang)
    w = get_i18n_msg("welcome_menu", lang)

    await state.set_state(AppState.main)
    await message.answer(f"{accept}\n{w}", reply_markup=menu_kb(lang))


@router.message(
    F.text.in_(("🌐 Tilni o'zgartirish", "🌐 Сменить язык", "🌐 Change language"))
)
async def change_lang(message: Message, state: FSMContext):
    msg = (
        "Please, choose language.\n"
        "Пожалуйста, выберите язык.\n"
        "Iltimos, tilni tanlang.\n"
    )

    await state.set_state(AppState.choose_lang)
    await message.answer(
        msg,
        reply_markup=LANG_KB,
    )
