from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext

from .db import db_helper
from .db.crud import get_user

from .core.load import get_bot
from .middleware import UserExistsMiddleware
from .keyboard.reply import LANG_KB
from .handler import main_router
from .state import AppState

dp = Dispatcher(storage=MemoryStorage())

async def start_bot() -> None:
    """Start the bot and set up the dispatcher."""

    bot = get_bot()

    dp.include_router(main_router)

    await dp.start_polling(bot)


@dp.message(CommandStart(), F.chat.type == "private")
@dp.message(
    F.text.in_(("🌐 Tilni o'zgartirish", "🌐 Сменить язык")) & F.chat.type == "private"
)
async def cmd_start(message: Message, state: FSMContext):
    user = message.from_user

    if message.text.startswith("/"):
        msg = (
            f"Salom, <b>{user.first_name}</b>!\n"
            "Iltimos, tilni tanlang.\n\n"
            f"Привет, <b>{user.first_name}</b>!\n"
            "Пожалуйста, выберите язык.\n\n"
        )
    else:
        msg = "Пожалуйста, выберите язык.\n" "Iltimos, tilni tanlang.\n"

    await state.set_state(AppState.choose_lang)
    await message.answer(
        msg,
        reply_markup=LANG_KB,
    )


@dp.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user

    start_msg = (
        f"Salom, <b>{user.first_name}</b>!\n"
        "⚠️ Bu bot guruhda ishlamaydi.\n\n"
        f"Привет, <b>{user.first_name}</b>!\n"
        "⚠️ Этот бот не работает в группах.\n\n"
    )

    await message.answer(start_msg)
