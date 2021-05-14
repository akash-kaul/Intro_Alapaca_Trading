import config as cf
import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt

# Base URL for fetching data, portfolio, etc. from Alpaca
BASE_URL = "https://paper-api.alpaca.markets"

# Create REST API connection
api = tradeapi.REST(key_id=cf.ALPACA_API_KEY,
                    secret_key=cf.ALPACA_SECRET_KEY, base_url=BASE_URL, api_version='v2')

# Fetch Apple data from last 100 days
APPLE_DATA = api.get_barset('AAPL', 'day', limit=100).df

# Preview Data
print(APPLE_DATA.head())

# Reformat data (drop multiindex, rename columns, reset index)
APPLE_DATA.columns = APPLE_DATA.columns.to_flat_index()
APPLE_DATA.columns = [x[1] for x in APPLE_DATA.columns]
APPLE_DATA.reset_index(inplace=True)
print(APPLE_DATA.head())

# Plot stock price data
plot = APPLE_DATA.plot(x="time", y="close", legend=False)
plot.set_xlabel("Date")
plot.set_ylabel("Apple Close Price ($)")
plt.show()
