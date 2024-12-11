import datetime

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from markdown_it.rules_core import inline

from database import create_db_pool


def menu_kb():
    kb = [
        [
            KeyboardButton(text="Student"),
            KeyboardButton(text="Owner")
        ],
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Tanlang"
    )

    return keyboard


async def admin_kb(user_id):
    pool = await create_db_pool()
    async with pool.acquire() as connection:
        user_type = await connection.fetchval(
            "SELECT user_type FROM users WHERE user_id = $1",
            user_id
        )

    if user_type == 'owner':
        kb = [
            [
                KeyboardButton(text="📂 Listings")
            ],
            [
                KeyboardButton(text="📃 Housing")
            ],
        ]
    else:
        kb = [
            [
                KeyboardButton(text="🔍 Search")
            ]
        ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    return keyboard


def inline_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="☑ Accept", callback_data="accept_housing"),
            InlineKeyboardButton(text="✖ Reject", callback_data="reject_housing")
        ]
    ]
    )
    return kb


def cancel_kb():
    kb = [
        [
            KeyboardButton(text="🔙 Bekor qilish")
        ]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    return keyboard


def location_keyboard():
    kb = [
        [
            KeyboardButton(text="Lokatsiyani yuboring", request_location=True)
        ]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return keyboard


def app_inline_kb(housing_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Application",
                callback_data=f"application_{housing_id}"
            )
        ]
    ])
    return kb


# KALENDAR BUTTON
def generate_calendar():
    today = datetime.date.today()
    current_month = today.month
    current_year = today.year
    days_in_month = [datetime.date(current_year, current_month, day) for day in range(1, 32)
                     if datetime.date(current_year, current_month, day).month == current_month]

    buttons = []
    row = []
    for i, day in enumerate(days_in_month, start=1):
        button = KeyboardButton(day.day)
        row.append(button)

        if i % 7 == 0 or i == len(days_in_month):  # Start a new row after every 7 days (week)
            buttons.append(row)
            row = []

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

