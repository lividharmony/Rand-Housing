
import json
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from handlers.keyboards import cancel_kb, admin_kb, app_inline_kb

from database import create_db_pool
from aiogram.types import Message, InputFile
from handlers.states import SearchState
import constants

router = Router()


@router.message(F.text == "🔙 Bekor qilish")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    await state.clear()

    await message.answer(
        text=constants.cancel_kb_message,
        reply_markup=await admin_kb(message.from_user.id),
    )


@router.message(F.text == "🔍 Search")
async def start_search(message: Message, state: FSMContext):
    await message.answer(constants.start_search_message, reply_markup=cancel_kb())
    await state.set_state(SearchState.search_query)


@router.message(SearchState.search_query)
async def handle_search_query(message: Message, state: FSMContext):
    search_query = message.text
    pool = await create_db_pool()

    async with pool.acquire() as connection:
        housings = await connection.fetch(
            "SELECT id, description, price, photo, location, duration FROM housings "
            "WHERE description ILIKE $1 OR price::text ILIKE $1",
            f"%{search_query}%"
        )

    if not housings:
        await message.answer(constants.no_housing_found_message)
    else:
        for housing in housings:
            housing_id = housing.get('id')
            if not housing_id:
                await message.answer(constants.housing_id_is_missing_message)
                continue

            location = housing['location']
            if location:
                try:
                    location_data = json.loads(location)
                    latitude = location_data.get('latitude')
                    longitude = location_data.get('longitude')

                    if latitude and longitude:
                        location_url = f"https://maps.google.com/?q={latitude},{longitude}"
                        location_text = f"[View on Google Maps]({location_url})"
                    else:
                        location_text = constants.location_info_not_full_message
                except json.JSONDecodeError:
                    location_text = constants.wrong_location_info_message
            else:
                location_text = constants.no_location_message

            await message.answer(
                f"Description🟰 {housing['description']}\n"
                f"Price🟰 {housing['price']} USD\n"
                f"Duration🟰 {housing['duration']} months\n"
                f"Location🟰 {location_text}",
                reply_markup=app_inline_kb(housing_id)
            )
    await state.clear()

