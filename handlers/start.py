from aiogram import Router, types
from aiogram.filters import CommandStart
import constants

router = Router()


@router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer(constants.bot_start_message)
