from aiogram import Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext

from .db import db_helper
from .db.crud import get_users

from .core.load import get_bot
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


@dp.message(Command("users"), F.chat.type.in_(("group", "supergroup")))
async def cmd_users(message: Message):
    msg = "👥Foydalanuvchilar:\n\n"
    async with db_helper.session_factory() as session:
        users = await get_users(session)

    i = 0
    for user in users:
        i += 1
        msg += f"👤Foydalanuvchi {i}: {user.name} | {user.phone_num} | {user.username}\n"

    msg += f"\nJami foydalanuvhcilar soni: {i}"

    await message.answer(msg)
