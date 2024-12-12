from aiogram import Router, types, F
from aiogram.types import Message

import constants
from database import create_db_pool
from handlers.keyboards import admin_kb

router = Router()


@router.message(F.text == "📂 Listings")
async def list_all_housings(message: Message):
    pool = await create_db_pool()
    user_id = message.from_user.id
    async with pool.acquire() as connection:
        housings = await connection.fetch(
            "SELECT description, price, location, duration FROM housings WHERE available = TRUE"
        )
    await pool.close()
    if not housings:
        await message.answer(constants.if_not_housings_message)
    else:
        for housing in housings:
            await message.answer(
                f"Description🟰 {housing['description']}\n"
                f"Price🟰 {housing['price']} USD\n"
                f"Location🟰 {housing['location']}\n"
                f"Duration🟰 {housing['duration']} months"
            )

    await message.answer(constants.list_all_housings_done_message, reply_markup=await admin_kb(message.from_user.id))
