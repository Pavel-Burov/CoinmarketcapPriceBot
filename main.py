import asyncio
import logging
from bot import send_crypto_report
from crypto_parser import fetch_crypto_data


async def main():
    while True:
        try:
            crypto_data = await fetch_crypto_data()
            await send_crypto_report(crypto_data)
            logging.info("Crypto data updated and sent to Telegram.")
        except Exception as e:
            logging.error(f"Error during data update: {e}")
        await asyncio.sleep(3 * 3600)  # 3 hours

if __name__ == '__main__':
    logging.basicConfig(filename="logs/app.log", level=logging.INFO)
    asyncio.run(main())
