from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(F.text.in_(("🔍 Kod yordamida qidirish", "🔍 Искать с помощью кода", "🔍 Search by code")))
async def search_by_code(message: Message, state: FSMContext):
    ...
    
@router.message(F.text.in_(("🧾 Katalog", "🧾 Каталог", "🛒 Корзина")))
async def catalog(message: Message, state: FSMContext):
    ...
    
@router.message(F.text.in_(("❤️ Sevimlilar", "❤️ Любимые", "❤️ Favorites")))
async def favorites(message: Message, state: FSMContext):
    ...