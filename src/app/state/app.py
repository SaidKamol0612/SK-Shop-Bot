from aiogram.fsm.state import StatesGroup, State

class AppState(StatesGroup):
    choose_lang = State()
    waiting_for_phone_number = State()
    main = State()
    choose_category = State()
    choose_product = State()
    product_details = State()
    show_favorites = State()
    show_products_in_cart = State()