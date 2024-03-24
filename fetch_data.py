"""API Specific Instructions 

Follow the docstring(s) below.
"""

import requests
import ccxt

def fetch_data():
    """Data Collections
    """

    # Coin names in alphabetical order
    cryptos = ['bitcoin', 'ethereum', 'polygon', 'solana', 'xrp']

    bitcoin_prices = []
    ethereum_prices = []
    polygon_prices = []
    solana_prices = []
    xrp_prices = []
    coins_price_list = [bitcoin_prices, ethereum_prices, polygon_prices, solana_prices, xrp_prices]

    # Exchange names in alphabetical order
    exchanges = ['Binance', 'Bitstamp', 'Gemini', 'Kraken', 'Poloniex']

    # initialize exchanges with ccxt
    binanceus_exchange = ccxt.binanceus()
    bitstamp_exchange = ccxt.bitstamp()
    gemini_exchange = ccxt.gemini()
    kraken_exchange = ccxt.kraken()
    poloniex_exchange = ccxt.poloniex()

    # Initialize tickers list per exchange 
    binance_tickers = ['BTCUSDT', 'ETHUSDT', 'MATICUSDT', 'SOLUSDT', 'XRPUSDT']
    bitstamp_tickers=['btcusd','ethusd','maticusd','solusd','xrpusd']
    kraken_tickers = ['XBTUSDT', 'ETHUSDT', 'MATICUSDT', 'SOLUSDT', 'XRPUSDT']
    gemini_tickers=['btcusd','ethusd','maticusd','solusd','xrpusd']
    poloniex_tickers = ['BTC_USDT', 'ETH_USDT', 'MATIC_USDT', 'SOL_USDT', 'XRP_USDT']

    # Initialize price lists 
    binance_prices = []
    poloniex_prices = []
    kraken_prices = []
    gemini_prices=[]
    bitstamp_prices=[]

    # All data lists 
    exchange_init = [binanceus_exchange, bitstamp_exchange, gemini_exchange, kraken_exchange, poloniex_exchange]
    tickers_init = [binance_tickers, bitstamp_tickers, gemini_tickers, kraken_tickers,  poloniex_tickers]
    exchange_prices_init = [binance_prices, bitstamp_prices, gemini_prices, kraken_prices, poloniex_prices]

    for i in range(len(exchanges)):
        for j in range(len(cryptos)):
            try:
                ticker = exchange_init[i].fetch_ticker(tickers_init[i][j])
                ask_price = float(ticker['ask'])
                bid_price = float(ticker['bid'])
                exchange_prices_init[i].append([ask_price, bid_price])
            except (requests.exceptions.RequestException, KeyError, IndexError, ValueError) as e:
                print(f'Error fetching data from {tickers_init[j]}: {e}')
                exchange_prices_init[j].append([None, None])

    for i in range(len(cryptos)):
        for j in range(len(exchange_prices_init)):
            try:
                coins_price_list[i].append(exchange_prices_init[j][i])
            except Exception as e:
                print(f'The following error occured when appending coins_price_list: {e}')
    
    return cryptos, exchanges, coins_price_list