import asyncio
import os
from http.client import responses

import aiofiles
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, User, BotCommand, CallbackQuery
from aiohttp import ClientResponseError

from inline_keyboards import get_weather_keyboard_inline
from reply_keyboard import get_weather_keyboard
from utils import config_logger, COMMANDS
from weather import WeatherHandler, USER_LOCATION_STORAGE

TOKEN = os.getenv("TOKEN")
dp = Dispatcher()
bot = Bot(TOKEN)
logger = config_logger()

class BotStates(StatesGroup):
    wait_city_name = State()
    play_games = State()
    default = State()


@dp.message(CommandStart())
async def start_command(message: Message):
    logger.info(f"User send /start to bot"
                f"Message(id={message.message_id}, text={message.text},"
                f"from={message.from_user.id}")

    user: User = message.from_user


    logger.info(f"User info: User(id={user.id}, "
                f"name={user.full_name}, "
                f"username={user.username},"
                f"photos={user.get_profile_photos()}")
    response_text = f"""
    Hello, {user.full_name}, I am beetroot bot. Nice to meet you! Your id = {user.id}
    """
    await bot.set_my_commands(COMMANDS + [BotCommand(command="cmd_for_you", description="TEst")])

    await message.answer(text=response_text, reply_markup=get_weather_keyboard())


@dp.message(F.text == "Get Bot Info")
async def get_bot_information(message: Message):
    await message.answer(f"I am {await bot.get_my_name()} with id={bot.id}")

@dp.message(F.text == "Get My ID")
async def get_bot_information(message: Message):
    await message.answer(f"You are {message.from_user.full_name} with id={message.from_user.id}")

@dp.message(F.text == "Get Weather")
async def get_bot_information(message: Message, state: FSMContext):
    # await state.set_state(BotStates.wait_city_name)
    # await message.answer("Send sity name:")
    try:
        weather = await (WeatherHandler().get_current(USER_LOCATION_STORAGE.get(message.from_user.id, "Unknown Location")))
        await message.answer(weather.as_text())
    except ClientResponseError as exc:
        await message.answer(f"Error while getting weather: {exc.message}")
    finally:
        await state.clear()

@dp.message(BotStates.wait_city_name)
async def get_weather_for_city(message: Message, state: FSMContext):
    try:
        weather = await (WeatherHandler().get_current(message.text))
        await message.answer(weather.as_text())
    except ClientResponseError as exc:
        await message.answer(f"Error while getting weather: {exc.message}")
    finally:
        await state.clear()

@dp.message(F.text == "Get Weather Inline")
async def inline_weather(message: Message):
    await message.answer(text="Bot Controller", reply_markup=get_weather_keyboard_inline())

@dp.callback_query(F.data == "get_weather")
async def get_weather_from_callback(callback: CallbackQuery):
    print(callback)
    try:
        weather = await (WeatherHandler().get_current(USER_LOCATION_STORAGE.get(callback.from_user.id, "Unknown Location")))
        await callback.message.edit_text(text=weather.as_text(), reply_markup=get_weather_keyboard_inline())
    except ClientResponseError as exc:
        await callback.message.edit_text(text=f"Error while getting weather: {exc.status}", reply_markup=get_weather_keyboard_inline())

@dp.callback_query(F.data == "get_user_id")
async def get_weather_from_callback(callback: CallbackQuery):
    response_text = f"Your id is {callback.from_user.id}"
    await callback.message.edit_text(text=response_text, reply_markup=get_weather_keyboard_inline())

@dp.callback_query(F.data == "get_bot_info")
async def get_weather_from_callback(callback: CallbackQuery):
    response_text = f"Bot name is {await bot.get_my_name()} , {await bot.get_my_description()}"
    await callback.message.edit_text(text=response_text, reply_markup=get_weather_keyboard_inline())

@dp.callback_query(F.data == "exit")
async def get_weather_from_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()

@dp.callback_query(F.data == "play")
async def get_weather_from_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BotStates.play_games)
    message = await callback.message.answer_dice("🎯")
    await state.set_data({"dice_value": message.dice.value})


@dp.message(BotStates.play_games)
async def get_dice(message: Message, state: FSMContext):
    bot_result = await state.get_value("dice_value")
    user_result = message.dice.value
    if bot_result > user_result:
        response_text = f"I win {bot_result}-{user_result}"
    elif bot_result < user_result:
        response_text = f"You win {bot_result}-{user_result}"
    else:
        response_text = f"Draw {bot_result}-{user_result}"

    await message.answer(response_text)
    # await bot.send_message()



@dp.message()
async def all_messages_handler(message: Message):
    with open("images.png") as file:
        await message.answer_photo(photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRURDX2GVjqOkWnWkOF9qDO9vK_BvT_Lxghag&s", caption="Send image")
    await message.answer(f"Message with text '{message.text}' is not supported")

async def main():
    await bot.set_my_commands(COMMANDS)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("Start Bot")
    asyncio.run(main())