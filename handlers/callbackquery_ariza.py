import logging
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from database import create_db_pool
from config import ADMINS

router = Router()


@router.callback_query(F.data.startswith("application_"))
async def application_callback(callback: CallbackQuery, state: FSMContext):
    housing_id = callback.data.split("_")[1]
    if not housing_id.isdigit():
        await callback.answer("⚠️Noto'g'ri uy-joy ID!")
        return

    housing_id = int(housing_id)
    user_id = callback.from_user.id
    pool = await create_db_pool()

    async with pool.acquire() as connection:
        user = await connection.fetchrow("SELECT id FROM users WHERE user_id = $1", user_id)
        if not user:
            await connection.execute(
                "INSERT INTO users (phone, name, user_id, user_type) VALUES ($1, $2, $3, $4)",
                "Unknown", "Anonymous", user_id, "student"
            )

        try:
            await connection.execute(
                "INSERT INTO applications (user_id, housing_id) "
                "VALUES ((SELECT id FROM users WHERE user_id = $1), $2)",
                user_id, housing_id
            )
        except Exception as e:
            logging.error(f"Error inserting application: {e}")
            await callback.answer("⚠️Arizangizni saqlashda xatolik yuz berdi.")
            return
        owner = await connection.fetchrow(
            "SELECT u.user_id FROM housings h JOIN users u ON h.owner_id = u.user_id WHERE h.id = $1",
            housing_id
        )

        if owner and owner['user_id']:
            owner_id = int(owner['user_id'])
            await callback.bot.send_chat_action(chat_id=owner_id, action="typing")
            logging.error(f"{owner_id}")
            await callback.bot.send_message(
                chat_id=owner_id,
                text=f"♥️Yangi ariza tushdi❗\n"
                     f"👨🏻 Foydalanuvchi ID: {user_id},\n 🏠 Uy-joy ID: {housing_id}"
                )
    await state.clear()
    await callback.answer("🤝 Arizangiz qabul qilindi!")
