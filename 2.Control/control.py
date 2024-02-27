import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.inspection import inspect
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String

# Global Variables 
wallet = 0

# Load environment variables from .env file
load_dotenv()

# Access the variables 
psql_username = os.getenv('PSQL_USERNAME')
psql_password = os.getenv('PSQL_PASSWORD')
psql_host = os.getenv('PSQL_HOST')
psql_port = os.getenv('PSQL_PORT')
db_name = os.getenv('DB_NAME')

# Define the database url
db_url = f"postgresql://{psql_username}:{psql_password}@{psql_host}:{psql_port}/{db_name}" 

# Create the engine object
engine = create_engine(db_url) 

# Create the table schema 
metadata = MetaData()

control = Table(
    'control',
    metadata,
    Column('trade_count', Integer, primary_key=True),
    Column('current_datetime', String),
    Column('currency', String),
    Column('volume', Float),
    Column('buy_exchange', String),
    Column('buy_price', Float),
    Column('total_purchase_amount', Float),
    Column('sell_exchange', String),
    Column('sell_price', Float),
    Column('total_sale_amount', Float),
    Column('profit', Float),
    Column('spread_percentage', Float)
)

# Execute the table creation
# Check if the table exist before creating
if not inspect(engine).has_table('control'):
    metadata.create_all(engine)

# Define arbitrage function
def find_arbitrage(exchange_a, exchange_b):
    ask_price_a = exchange_a[0]
    bid_price_b = exchange_b[1]

    spread_percent = (bid_price_b - ask_price_a) / ask_price_a * 100

    return spread_percent, ask_price_a, bid_price_b


# Define main function
def main():
    ######
    ######
    ######
    # Set the current time
    current_datetime = datetime.now().isoformat()

    ######
    ######
    ######
    # Fetch all the data
    # Binance data
    binance_tickers = ['BTCUSDT', 'ETHUSDT', 'MATICUSDT', 'SOLUSDT', 'XRPUSDT']
    binance_api_url = 'https://api.binance.us/api/v3/ticker/bookTicker?symbol='

    binance_prices = []

    for i in range(len(binance_tickers)):
        api_url = binance_api_url+binance_tickers[i]
        api_response = requests.get(api_url).json()
        ask_price = float(api_response['askPrice'])
        bid_price = float(api_response['bidPrice'])
        binance_prices.append([ask_price, bid_price])

    # Bitstamp data
    bitstamp_tickers=['btcusd','ethusd','maticusd','solusd','xrpusd']
    bitstamp_api_url= 'https://www.bitstamp.net/api/v2/ticker/'

    bitstamp_prices=[]

    for i in range(len(bitstamp_tickers)):
        api_url=bitstamp_api_url+bitstamp_tickers[i]
        api_response=requests.get(api_url).json()
        ask_price=float(api_response['ask'])
        bid_price=float(api_response['bid'])
        bitstamp_prices.append([ask_price,bid_price])

    # Gemini data
    gemini_tickers=['btcusd','ethusd','maticusd','solusd','xrpusd']
    gemini_api_url= 'https://api.gemini.com/v2/ticker/'

    gemini_prices=[]

    for i in range(len(gemini_tickers)):
        api_url=gemini_api_url+gemini_tickers[i]
        api_response=requests.get(api_url).json()
        ask_price=float(api_response['ask'])
        bid_price=float(api_response['bid'])
        gemini_prices.append([ask_price,bid_price])

    # Kraken data
    kraken_tickers = ['XBTUSDT', 'ETHUSDT', 'MATICUSDT', 'SOLUSDT', 'XRPUSDT']
    kraken_api_url = 'https://api.kraken.com/0/public/Ticker?pair='

    kraken_prices = []

    for i in range(len(kraken_tickers)):
        api_url = kraken_api_url+kraken_tickers[i]
        api_response = requests.get(api_url).json()
        ask_price = float(api_response['result'][kraken_tickers[i]]['a'][0])
        bid_price = float(api_response['result'][kraken_tickers[i]]['b'][0])
        kraken_prices.append([ask_price, bid_price])

    # Poloniex data
    poloniex_tickers = ['BTC_USDT', 'ETH_USDT', 'MATIC_USDT', 'SOL_USDT', 'XRP_USDT']
    poloniex_api_url = "https://api.poloniex.com/markets/"

    poloniex_prices = []

    for i in range(len(poloniex_tickers)):
        api_url = poloniex_api_url+poloniex_tickers[i]+"/orderBook"
        api_response = requests.get(api_url).json()
        ask_price = float(api_response['asks'][0])
        bid_price = float(api_response['bids'][0])
        poloniex_prices.append([ask_price, bid_price])

    ######
    ######
    ######
    # Store data for easy retrival
    cryptos = ['bitcoin', 'ethereum', 'polygon', 'solana', 'xrp']

    bitcoin_prices = [binance_prices[0], bitstamp_prices[0], gemini_prices[0], kraken_prices[0], poloniex_prices[0]]
    ethereum_prices = [binance_prices[1], bitstamp_prices[1], gemini_prices[1], kraken_prices[1], poloniex_prices[1]]
    polygon_prices = [binance_prices[2], bitstamp_prices[2], gemini_prices[2], kraken_prices[2], poloniex_prices[2]]
    solana_prices = [binance_prices[3], bitstamp_prices[3], gemini_prices[3], kraken_prices[3], poloniex_prices[3]]
    xrp_prices = [binance_prices[4], bitstamp_prices[4], gemini_prices[4], kraken_prices[4], poloniex_prices[4]]

    exchanges = ['Binance', 'Bitstamp', 'Gemini', 'Kraken', 'Poloniex']

    ######
    ######
    ######
    # Set share per coin to a unit (1 share)
    bitcoin_shares = 1
    ethereum_shares = 1
    polygon_shares = 1
    solana_shares = 1
    xrp_shares = 1

    # Bitcoin Trades
    for i in range(len(bitcoin_prices)):
        for j in range(i+1, len(bitcoin_prices)):
            exchange_a, exchange_b = bitcoin_prices[i], bitcoin_prices[j]
            exchange_name_a, exchange_name_b = exchanges[i], exchanges[j]

            spread_percentage, buy_price, sell_price = find_arbitrage(exchange_a, exchange_b)

            if spread_percentage > 0:
                current_datetime
                purchase_price = bitcoin_shares*buy_price
                sale_price = bitcoin_shares*sell_price
                profit = sale_price - purchase_price
                
                insert_row = control.insert().values(
                    current_datetime = current_datetime,
                    currency = cryptos[0],
                    volume = bitcoin_shares,
                    buy_exchange = exchange_name_a,
                    buy_price = buy_price,
                    total_purchase_amount = purchase_price,
                    sell_exchange = exchange_name_b,
                    sell_price = sell_price,
                    total_sale_amount = sale_price,
                    profit = profit,
                    spread_percentage = spread_percentage
                )

                with engine.connect() as connection:
                    connection.execute(insert_row)
                        
    # Ethereum Trades
    for i in range(len(ethereum_prices)):
        for j in range(i+1, len(ethereum_prices)):
            exchange_a, exchange_b = ethereum_prices[i], ethereum_prices[j]
            exchange_name_a, exchange_name_b = exchanges[i], exchanges[j]

            spread_percentage, buy_price, sell_price = find_arbitrage(exchange_a, exchange_b)

            if spread_percentage > 0:
                current_datetime
                purchase_price = ethereum_shares*buy_price
                sale_price = ethereum_shares*sell_price
                profit = sale_price - purchase_price
                
                insert_row = control.insert().values(
                    current_datetime = current_datetime,
                    currency = cryptos[1],
                    volume = ethereum_shares,
                    buy_exchange = exchange_name_a,
                    buy_price = buy_price,
                    total_purchase_amount = purchase_price,
                    sell_exchange = exchange_name_b,
                    sell_price = sell_price,
                    total_sale_amount = sale_price,
                    profit = profit,
                    spread_percentage = spread_percentage
                )

                with engine.connect() as connection:
                    connection.execute(insert_row)

    # Polygon Trades
    for i in range(len(polygon_prices)):
        for j in range(i+1, len(polygon_prices)):
            exchange_a, exchange_b = polygon_prices[i], polygon_prices[j]
            exchange_name_a, exchange_name_b = exchanges[i], exchanges[j]

            spread_percentage, buy_price, sell_price = find_arbitrage(exchange_a, exchange_b)

            if spread_percentage > 0:
                current_datetime
                purchase_price = polygon_shares*buy_price
                sale_price = polygon_shares*sell_price
                profit = sale_price - purchase_price
                
                insert_row = control.insert().values(
                    current_datetime = current_datetime,
                    currency = cryptos[2],
                    volume = polygon_shares,
                    buy_exchange = exchange_name_a,
                    buy_price = buy_price,
                    total_purchase_amount = purchase_price,
                    sell_exchange = exchange_name_b,
                    sell_price = sell_price,
                    total_sale_amount = sale_price,
                    profit = profit,
                    spread_percentage = spread_percentage
                )

                with engine.connect() as connection:
                    connection.execute(insert_row)
                        
    # Solana Trades
    for i in range(len(solana_prices)):
        for j in range(i+1, len(solana_prices)):
            exchange_a, exchange_b = solana_prices[i], solana_prices[j]
            exchange_name_a, exchange_name_b = exchanges[i], exchanges[j]

            spread_percentage, buy_price, sell_price = find_arbitrage(exchange_a, exchange_b)

            if spread_percentage > 0:
                current_datetime
                purchase_price = solana_shares*buy_price
                sale_price = solana_shares*sell_price
                profit = sale_price - purchase_price
                
                insert_row = control.insert().values(
                    current_datetime = current_datetime,
                    currency = cryptos[3],
                    volume = solana_shares,
                    buy_exchange = exchange_name_a,
                    buy_price = buy_price,
                    total_purchase_amount = purchase_price,
                    sell_exchange = exchange_name_b,
                    sell_price = sell_price,
                    total_sale_amount = sale_price,
                    profit = profit,
                    spread_percentage = spread_percentage
                )

                with engine.connect() as connection:
                    connection.execute(insert_row)

    # XRP Trades
    for i in range(len(xrp_prices)):
        for j in range(i+1, len(xrp_prices)):
            exchange_a, exchange_b = xrp_prices[i], xrp_prices[j]
            exchange_name_a, exchange_name_b = exchanges[i], exchanges[j]

            spread_percentage, buy_price, sell_price = find_arbitrage(exchange_a, exchange_b)

            if spread_percentage > 0:
                current_datetime
                purchase_price = xrp_shares*buy_price
                sale_price = xrp_shares*sell_price
                profit = sale_price - purchase_price
                
                insert_row = control.insert().values(
                    current_datetime = current_datetime,
                    currency = cryptos[4],
                    volume = xrp_shares,
                    buy_exchange = exchange_name_a,
                    buy_price = buy_price,
                    total_purchase_amount = purchase_price,
                    sell_exchange = exchange_name_b,
                    sell_price = sell_price,
                    total_sale_amount = sale_price,
                    profit = profit,
                    spread_percentage = spread_percentage
                )

                with engine.connect() as connection:
                    connection.execute(insert_row)

    print('Trading in progress...')

######
######
######
# Define a function to loop the main function
def main_loop():  
    try:
        while True:
            main()          
            time.sleep(30)
    except KeyboardInterrupt:
        print("Program terminated by user.")

######
######
######
# Call function to run all code above
main_loop()