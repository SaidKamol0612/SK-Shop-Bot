from aiogram.fsm.state import StatesGroup, State

class AppState(StatesGroup):
    choose_lang = State()
    
    # Registration
    waiting_for_name = State()
    waiting_for_phone_number = State()
    
    # Main
    main = State()
    
    # Catalog
    choose_category = State()
    choose_product = State()
    product_details = State()
    
    # Favorites
    show_favorites = State()
    
    # Cart
    show_products_in_cart = State()
    
    # Search
    search_by_code = State()
    
    # Order
    waiting_confirm_order = State()