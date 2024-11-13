import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime


async def fetch_crypto_data(page):
    # Initialize list to hold the cryptocurrency data
    crypto_data = []

    # Loop to retrieve the top 10 cryptocurrencies
    for i in range(1, 11):  # Top 10 by trading volume
        # Define the selectors for each element
        name_selector = f"tbody > tr:nth-child({i}) > td:nth-child(3) > div > a > div > div > div > p"
        price_selector = f"tbody > tr:nth-child({i}) > td:nth-child(4) > div > span"
        change_24h_selector = f"tbody > tr:nth-child({i}) > td:nth-child(6) > span"
        volume_selector = f"tbody > tr:nth-child({i}) > td:nth-child(9) > div > a > p"

        # Extract text using the defined selectors
        name = await page.locator(name_selector).inner_text()
        price = await page.locator(price_selector).inner_text()
        change_24h = await page.locator(change_24h_selector).inner_text()
        volume = await page.locator(volume_selector).inner_text()

        # Append the data for this cryptocurrency to the list
        crypto_data.append({
            "name": name,
            "price": price,
            "change_24h": change_24h,
            "volume": volume
        })

    # Save the data with a timestamp to a JSON file
    data = {
        "last_update": datetime.utcnow().isoformat(),
        "data": crypto_data
    }
    with open("data/crypto_data.json", "w") as file:
        json.dump(data, file, indent=4)


async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(java_script_enabled=True)

        # Navigate to CoinMarketCap
        print("Go to website...")
        await page.goto("https://coinmarketcap.com/", timeout=60000)
        await page.wait_for_selector("table",  timeout=60000)

        return page
        # Close the browser
        # browser.close()

# To run the function
# asyncio.run(fetch_crypto_data())
