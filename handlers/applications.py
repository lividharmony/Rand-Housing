from aiogram import types, Router, Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from .keyboards import admin_kb
from .register import start_registration
import constants
router = Router()


@router.message(CommandStart())
async def apply_for_housing(message: types.Message, dispatcher: Dispatcher, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    pool = dispatcher['db']
    async with pool.acquire() as connection:
        result = await connection.fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)

        if result is None:
            await start_registration(message, state)
            return

    await message.answer(constants.hello_message, reply_markup=await admin_kb(message.from_user.id))
