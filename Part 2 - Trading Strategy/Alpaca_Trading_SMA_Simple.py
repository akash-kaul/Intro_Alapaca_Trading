import config as cf
import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt
import numpy as np

# Base URL for fetching data, portfolio, etc. from Alpaca
BASE_URL = "https://paper-api.alpaca.markets"

# Create REST API connection
api = tradeapi.REST(key_id=cf.ALPACA_API_KEY,
                    secret_key=cf.ALPACA_SECRET_KEY, base_url=BASE_URL, api_version='v2')

# Fetch Apple data from last 20 days
APPLE_DATA = api.get_barset('AAPL', 'day', limit=100).df

# Reformat data (drop multiindex, rename columns, reset index)
APPLE_DATA.columns = APPLE_DATA.columns.to_flat_index()
APPLE_DATA.columns = [x[1] for x in APPLE_DATA.columns]
APPLE_DATA.reset_index(inplace=True)

# Calculate moving averages
APPLE_DATA['20_SMA'] = APPLE_DATA['close'].rolling(window=20, min_periods=1).mean()
APPLE_DATA['10_SMA'] = APPLE_DATA['close'].rolling(window=10, min_periods=1).mean()

# Find crossover points
APPLE_DATA['Cross'] = 0.0
APPLE_DATA['Cross'] = np.where(APPLE_DATA['10_SMA'] > APPLE_DATA['20_SMA'], 1.0, 0.0)
APPLE_DATA['Signal'] = APPLE_DATA['Cross'].diff()

# Map numbers to words
map_dict = {-1.0: 'sell', 1.0: 'buy', 0.0: 'none'}
APPLE_DATA["Signal"] = APPLE_DATA["Signal"].map(map_dict)

# Preview Data
# print(APPLE_DATA.head())

# Show Relevant Buy/Sell data
print(APPLE_DATA[APPLE_DATA['Signal'] != 'none'].dropna())


# Plot stock price data
APPLE_DATA.plot(x="time", y=["close", "20_SMA", "10_SMA"], color=['k', 'b', 'm'])

# Plot ‘buy’ signals
plt.plot(APPLE_DATA[APPLE_DATA['Signal'] == 'buy']['time'],
         APPLE_DATA['20_SMA'][APPLE_DATA['Signal'] == 'buy'],
         '^', markersize=8, color='g', label='buy')

# Plot ‘sell’ signals
plt.plot(APPLE_DATA[APPLE_DATA['Signal'] == 'sell']['time'],
         APPLE_DATA['20_SMA'][APPLE_DATA['Signal'] == 'sell'],
         'v', markersize=8, color='r', label='sell')

plt.xlabel("Date")
plt.ylabel("Apple Close Price ($)")
plt.legend()
plt.show()
