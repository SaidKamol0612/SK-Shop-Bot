from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext

from .core.config import settings
from .keyboard.reply import LANG_KB
from .handler import main_router
from .state import AppState

dp = Dispatcher(storage=MemoryStorage())


async def start_bot() -> None:
    """Start the bot and set up the dispatcher."""

    bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp.include_router(main_router)

    await dp.start_polling(bot)


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user = message.from_user

    start_msg = (
        f"Salom, <b>{user.first_name}</b>!\n"
        "Iltimos, tilni tanlang.\n\n"
        f"Привет, <b>{user.first_name}</b>!\n"
        "Пожалуйста, выберите язык.\n\n"
        f"Hello, <b>{user.first_name}</b>!\n"
        "Please, choose language.\n\n"
    )

    await state.set_state(AppState.choose_lang)
    await message.answer(
        start_msg,
        reply_markup=LANG_KB,
    )
