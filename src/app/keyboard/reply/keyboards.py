from aiogram.utils.keyboard import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardBuilder,
)

from app.util.i18n import get_i18n_msg

LANG_KB = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🇺🇿 O'zbekcha"),
            KeyboardButton(text="🇷🇺 Русский"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


def send_phone_kb(lang: str):
    msg = get_i18n_msg("send_number", lang)

    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=msg, request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def menu_kb(lang: str) -> ReplyKeyboardMarkup:
    options = get_i18n_msg("menu", lang)
    kb = ReplyKeyboardBuilder()

    for option in options:
        kb.add(KeyboardButton(text=option))

    return kb.adjust(2).as_markup(resize_keyboard=True)


def catalog_kb(
    list_e: list[str], is_ctg: bool | None = False, lang: str = "uz"
) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()

    for e in list_e:
        if is_ctg:
            kb.add(KeyboardButton(text=e))
        else:
            kb.add(KeyboardButton(text=f"{e['name']} {e['id']}"))
    if not is_ctg:
        kb.add(KeyboardButton(text=get_i18n_msg("back_to_categories", lang)))

    kb.add(KeyboardButton(text=get_i18n_msg("back_to_menu", lang)))

    return kb.adjust(2).as_markup(resize_keyboard=True)


def main_kb(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_i18n_msg("back_to_menu", lang)),
            ],
        ],
        resize_keyboard=True,
    )

