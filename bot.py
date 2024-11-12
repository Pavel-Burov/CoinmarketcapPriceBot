from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import json
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not API_TOKEN or not CHAT_ID:
    raise ValueError(
        "BOT_TOKEN and CHAT_ID must be set in the environment variables.")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def send_crypto_report():
    try:
        with open('data/crypto_data.json') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading JSON data: {e}")
        return

    message = f"*Crypto Update (Last updated: {data['last_update']} UTC)*\n\n"
    for idx, crypto in enumerate(data["data"], 1):
        message += f"{idx}. {crypto['name']}: ${crypto['price']}, 24h: {crypto['change']}%, Volume: ${crypto['volume']}\n"

    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.MARKDOWN)


async def periodic_report(interval: int):
    while True:
        await send_crypto_report()
        await asyncio.sleep(interval)


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await message.reply("Crypto bot started! You will receive updates every 3 hours.")
    asyncio.create_task(periodic_report(3 * 60 * 60))


@dp.message_handler(commands=['stop'])
async def stop_bot(message: types.Message):
    await message.reply("Crypto bot stopped. You will no longer receive updates.")


@dp.message_handler(commands=['list'])
async def list_cryptos(message: types.Message):
    await send_crypto_report()


@dp.message_handler(commands=['currency'])
async def get_currency(message: types.Message):
    query = message.get_args().capitalize()
    try:
        with open('data/crypto_data.json') as file:
            data = json.load(file)
        crypto = next((c for c in data["data"] if c["name"] == query), None)
        if crypto:
            await message.reply(f"{crypto['name']}: ${crypto['price']}, 24h: {crypto['change']}%, Volume: ${crypto['volume']}")
        else:
            await message.reply(f"Cryptocurrency '{query}' not found.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        await message.reply("Error loading cryptocurrency data.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
