from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_weather_keyboard_inline():
    get_weather_btn = InlineKeyboardButton(text="Get Weather", callback_data=f"get_weather")
    get_user_id_btn = InlineKeyboardButton(text="Get My ID", callback_data="get_user_id")
    get_bot_info_btn = InlineKeyboardButton(text="Get Bot Info", callback_data="get_bot_info")
    play_btn = InlineKeyboardButton(text="Play", callback_data="play")
    exit_btn = InlineKeyboardButton(text="Exit", callback_data="exit")

    keyboard =InlineKeyboardMarkup(
        inline_keyboard =[
            [get_weather_btn, play_btn],
            [get_bot_info_btn, get_user_id_btn],
            [exit_btn]
        ]
    )
    return keyboard
