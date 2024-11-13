from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from crypto_parser import fetch_crypto_data
import json
import os
from dotenv import load_dotenv
import asyncio
load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)


async def send_crypto_report():
    await fetch_crypto_data()
    with open('data/crypto_data.json') as file:
        data = json.load(file)

    message = f"Crypto Update (Last updated: {data['last_update']} UTC)\n\n"

    for crypto in data["data"]:
        message += f"**{crypto['name']}:** {crypto['price']}, **Change 24h:** {crypto['change_24h']}, **Volume**: {crypto['volume']}\n"

    await bot.send_message(chat_id=os.getenv("CHAT_ID"), text=message, parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await message.reply("Crypto bot started! You will receive updates every 3 hours.")


@dp.message_handler(commands=['stop'])
async def stop_bot(message: types.Message):
    await message.reply("Crypto bot stopped. You will no longer receive updates.")


@dp.message_handler(commands=['list'])
async def list_cryptos(message: types.Message):
    await send_crypto_report()


@dp.message_handler(commands=['currency'])
async def get_currency(message: types.Message):
    query = message.get_args().capitalize()
    with open('data/crypto_data.json') as file:
        data = json.load(file)

    found = False
    for crypto in data["data"]:
        if crypto["name"] == query:
            await message.reply(f"{crypto['name']}: {crypto['price']}, 24h: {crypto['change_24h']}, Volume: {crypto['volume']}")
            found = True
            break

    if not found:
        await message.reply(f"Cryptocurrency '{query}' not found.")

executor.start_polling(dp, skip_updates=True)
