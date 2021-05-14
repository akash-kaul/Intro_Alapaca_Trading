import config as cf
import time
import alpaca_trade_api as tradeapi

# Base URL for fetching data, portfolio, etc. from Alpaca
BASE_URL = "https://paper-api.alpaca.markets"

# Create REST API connection
api = tradeapi.REST(key_id=cf.ALPACA_API_KEY,
                    secret_key=cf.ALPACA_SECRET_KEY, base_url=BASE_URL, api_version='v2')

# Submit Order to buy stock
api.submit_order(symbol='AAPL', qty=1, side='buy', type='market',
                 time_in_force='day')

# Wait before checking for live changes to your portfolio to give time for your account to update
time.sleep(5)

# # Get stock position
aapl_position = api.get_position('AAPL')
print(aapl_position)

# Submit Order to short stock
api.submit_order('TSLA', 1, 'sell', 'market', 'day')
time.sleep(5)

# Get stock position
tsla_position = api.get_position('TSLA')
print(tsla_position)

# Get a list of all of our positions.
portfolio = api.list_positions()

# Print the quantity of shares for each position.
for position in portfolio:
    print("{} shares of {}".format(position.qty, position.symbol))
