from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.util.i18n import get_i18n_msg


def product_kb(product_id: int, lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    product_menu = get_i18n_msg("product_menu", lang)

    kb.add(
        InlineKeyboardButton(
            text=product_menu[0], callback_data=f"like_unlike:{product_id}"
        ),
        InlineKeyboardButton(
            text=product_menu[1], callback_data=f"add_to_cart:{product_id}"
        ),
        InlineKeyboardButton(
            text=product_menu[2], callback_data=f"buy_now:{product_id}"
        ),
    )

    return kb.adjust(2).as_markup()
