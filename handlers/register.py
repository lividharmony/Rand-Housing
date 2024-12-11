import re

from aiogram import types, Router, F, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from database import create_db_pool
from handlers.keyboards import menu_kb
from handlers.states import UserForm

router = Router()


@router.message(CommandStart())
async def start_registration(message: types.Message, state: FSMContext):
    await state.set_state(UserForm.phone_number)
    await message.answer("Xush kelibsiz❗ Ro'yxatdan o'tish uchun telefon raqamingizni kiriting.")


@router.message(UserForm.phone_number)
async def handle_phone(message: types.Message, state: FSMContext):
    regex = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
    if re.fullmatch(regex, message.text):
        phone_number = message.text
        await state.update_data({"phone_number": phone_number})
        await message.answer(text="Siz Studentmisiz yoki Owner❓", reply_markup=menu_kb())
        await state.set_state(UserForm.user_type)
    else:
        await message.answer("❌ telefon xato")


@router.message(UserForm.user_type)
async def handle_user_type(message: types.Message, state: FSMContext):
    user_type = message.text.lower()
    user_data = await state.get_data()
    await state.clear()

    pool = await create_db_pool()
    async with pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO users (phone, name, user_id, user_type) VALUES ($1, $2,$3,$4) ON CONFLICT (phone) DO NOTHING",
            user_data["phone_number"], message.from_user.full_name, message.from_user.id, user_type
        )
    await pool.close()

    await message.answer("✔️Siz muvaffaqiyatli ro'yxatdan o'tdingiz!")
