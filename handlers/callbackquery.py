import json
import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from database import create_db_pool
from handlers.keyboards import admin_kb


router = Router()


@router.callback_query(F.data == "accept_housing")
async def confirm_housing(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    logging.info("Data in confirm_housing: %s", data)

    description = data.get("description")
    price = data.get("price")
    photo = data.get("photo")
    location = data.get("location")
    duration = data.get("duration")

    location_json = json.dumps({'latitude': location['latitude'], 'longitude': location['longitude']})
    print("description", description, "price", price, "location", location)

    if None in (description, price, photo, location, duration):
        await callback.answer("Ma'lumotlar to'liq emas. Iltimos, qaytadan urinib ko'ring.")
        return

    pool = await create_db_pool()
    async with pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO housings (description, price, photo, location, duration, available, owner_id)"
            " VALUES ($1, $2, $3, $4, $5, TRUE, $6)",
            description, price, photo, location_json, duration, callback.from_user.id
        )

    await callback.message.delete()
    await callback.message.answer("✔ Uy-joy muvaffaqiyatli qo'shildi!",
                                  reply_markup=await admin_kb(callback.from_user.id))
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "reject_housing")
async def reject_housing(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    if callback.message and callback.message.text:
        await callback.message.edit_text(
            "❌ Ma'lumotlar bekor qilindi.",
            reply_markup=await admin_kb(callback.from_user.id)
        )
    else:
        await callback.message.answer(
            "❌ Ma'lumotlar bekor qilindi.",
            reply_markup=await admin_kb(callback.from_user.id)
        )
    await callback.answer()


