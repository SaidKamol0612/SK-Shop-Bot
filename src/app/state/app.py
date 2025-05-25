from aiogram.fsm.state import StatesGroup, State

from .registraion import RegistrationStates

class AppState(StatesGroup):
    choose_lang = State()
    main = State()