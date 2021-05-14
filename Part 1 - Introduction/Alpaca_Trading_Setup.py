import config as cf
import alpaca_trade_api as tradeapi

# Base URL for fetching data, portfolio, etc. from Alpaca
BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(key_id=cf.ALPACA_API_KEY,
                    secret_key=cf.ALPACA_SECRET_KEY, base_url=BASE_URL, api_version='v2')

# Create REST API connection
account = api.get_account()

print(account.id, '\n', account.equity, '\n', account.status)
