import logging
import os

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database import create_db_pool
from config import ADMINS
from handlers.keyboards import inline_kb, admin_kb, cancel_kb, location_keyboard, generate_calendar
from handlers.states import HousingForm

router = Router()


def filter_by_id(message: types.Message):
    return message.from_user.id in ADMINS


@router.message(F.text == "🔙 Bekor qilish")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Bekor qilindi",
        reply_markup=await admin_kb(message.from_user.id),
    )


@router.message(F.text == "📃 Housing")
async def start_admin_housing(message: types.Message, state: FSMContext):
    logging.info("Admin housing command received.")
    await message.answer("🖊 Uy-joy haqida qisqacha ma'lumot kiriting:", reply_markup=cancel_kb())
    await state.set_state(HousingForm.description)


@router.message(HousingForm.description)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    logging.info("Updated state with description: %s", message.text)
    await message.answer("💵 Narxni kiriting:")
    await state.set_state(HousingForm.price)


@router.message(HousingForm.price)
async def add_price(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.update_data(price=price)
        logging.info("Updated state with price: %s", price)
        await message.answer("📸 rasmni kiriting:")
        await state.set_state(HousingForm.photo)
    except ValueError:
        await message.answer("🙏🏽 Iltimos, narxni to'g'ri formatda kiriting (faqat son).")


@router.message(HousingForm.photo)
async def add_image(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("🙏🏽 Iltimos, rasmni jo'nating.")
        return
    photo_f = message.photo[-1]

    images_dir = "images"
    os.makedirs(images_dir, exist_ok=True)
    file_path = os.path.join(images_dir, f"{photo_f.file_unique_id}.jpg")
    file_info = await message.bot.get_file(photo_f.file_id)

    await message.bot.download_file(file_info.file_path, file_path)
    await state.update_data(photo=file_path, photo_id=photo_f.file_id)
    logging.info("Updated state with photo: %s", file_path)
    await message.answer("📍 Manzilni kiriting", reply_markup=location_keyboard())
    await state.set_state(HousingForm.location)


@router.message(HousingForm.location)
async def add_location(message: types.Message, state: FSMContext):
    if message.location:
        lat = message.location.latitude
        lon = message.location.longitude

        maps_url = f"https://maps.google.com/?q={lat},{lon}"

        await state.update_data(location={'latitude': lat, 'longitude': lon, 'maps_url': maps_url})
        logging.info("Updated state with location: %s", {'latitude': lat, 'longitude': lon, 'maps_url': maps_url})
        await message.answer("🗓 Muddatni oyda kiriting (masalan, 6):")
        await state.set_state(HousingForm.duration)
    else:
        await message.answer("🙏🏽 Iltimos, lokatsiyani yuboring.")


@router.message(HousingForm.duration)
async def add_duration(message: types.Message, state: FSMContext):
    try:
        duration = int(message.text)
        await state.update_data(duration=duration)

        data = await state.get_data()
        logging.info("Data: %s", data)

        description = data["description"]
        price = data["price"]
        photo = data["photo"]
        location = data["location"]
        duration = data["duration"]
        photo_id = data["photo_id"]

        await message.answer_photo(
            photo=photo_id,
            caption=f"✔ Uy-joy muvaffaqiyatli qo'shildi!\n\n"
                    f"Description: {description}\nPrice:"
                    f" {price}\nLocation: {location}\nDuration: {duration} months\nImage path: {photo}",
            reply_markup=inline_kb()
        )
    except ValueError:
        await message.answer("🙏🏽 Iltimos, muddatni to'g'ri formatda kiriting (faqat son).")
