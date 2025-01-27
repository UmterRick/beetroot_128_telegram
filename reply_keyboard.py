from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_weather_keyboard():
    get_weather_btn = KeyboardButton(text="Get Weather")
    get_weather_btn = KeyboardButton(text="Get Weather Inline")
    get_user_id_btn = KeyboardButton(text="Get My ID")
    get_bot_info_btn = KeyboardButton(text="Get Bot Info")
    exit_btn = KeyboardButton(text="Exit")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [get_weather_btn,get_user_id_btn],
            [exit_btn, get_bot_info_btn]
        ]
    )
    return keyboard