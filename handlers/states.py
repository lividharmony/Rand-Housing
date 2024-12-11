from aiogram.fsm.state import StatesGroup, State


class UserForm(StatesGroup):
    phone_number = State()
    user_type = State()


class AdminForm(StatesGroup):
    add_housing = State()
    save_housing = State()


class HousingForm(StatesGroup):
    description = State()
    price = State()
    photo = State()
    photo_id = State()
    location = State()
    duration = State()


class SearchState(StatesGroup):
    search_query = State()
