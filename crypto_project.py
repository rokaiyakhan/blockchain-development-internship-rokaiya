import requests

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",  # Fetch data in USD
        "order": "market_cap_desc",  # Order by market capitalization
        "per_page": 50,  # Top 50 cryptocurrencies
        "page": 1,
        "sparkline": False
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:  # Success
        return response.json()  # Return the data as JSON
    else:
        print("Error fetching data:", response.status_code)
        return None

import pandas as pd

def analyze_data(crypto_data):
    # Convert to DataFrame
    df = pd.DataFrame(crypto_data)
    df = df[["name", "symbol", "current_price", "market_cap", "total_volume", "price_change_percentage_24h"]]

    # Top 5 by market capitalization
    top_5 = df.nlargest(5, "market_cap")

    # Average price
    avg_price = df["current_price"].mean()

    # Highest and lowest 24-hour percentage change
    max_change = df["price_change_percentage_24h"].max()
    min_change = df["price_change_percentage_24h"].min()

    print("Top 5 Cryptocurrencies by Market Cap:\n", top_5)
    print("Average Price of Top 50 Cryptos: $", avg_price)
    print("Highest 24h Change: ", max_change, "%")
    print("Lowest 24h Change: ", min_change, "%")

    return df

def update_excel(df, filename="crypto_data.xlsx"):
    df.to_excel(filename, index=False, engine="openpyxl")
    print(f"Data updated in {filename}")

import time

def live_update():
    while True:
        crypto_data = fetch_crypto_data()
        if crypto_data:
            df = analyze_data(crypto_data)
            update_excel(df)
        time.sleep(300)  # Wait for 5 minutes (300 seconds)


# Test the function
crypto_data = fetch_crypto_data()
if crypto_data:
    print(f"Fetched {len(crypto_data)} cryptocurrencies!")
    print("Sample Data:", crypto_data[0])  # Print the first cryptocurrency

# Process and analyze
if crypto_data:
    df = analyze_data(crypto_data)

# Save the data to Excel
if crypto_data:
    update_excel(df)

# Start live updates
live_update()