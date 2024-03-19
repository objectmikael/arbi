import requests

def fetch_data():

    # Exchange names in alphabetical order
    exchanges = ['Binance', 'Bitstamp', 'Gemini', 'Kraken', 'Poloniex']


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

    bitcoin_prices = [binance_prices[0], bitstamp_prices[0], gemini_prices[0], kraken_prices[0], poloniex_prices[0]]
    ethereum_prices = [binance_prices[1], bitstamp_prices[1], gemini_prices[1], kraken_prices[1], poloniex_prices[1]]
    polygon_prices = [binance_prices[2], bitstamp_prices[2], gemini_prices[2], kraken_prices[2], poloniex_prices[2]]
    solana_prices = [binance_prices[3], bitstamp_prices[3], gemini_prices[3], kraken_prices[3], poloniex_prices[3]]
    xrp_prices = [binance_prices[4], bitstamp_prices[4], gemini_prices[4], kraken_prices[4], poloniex_prices[4]]

    # Coin names in alphabetical order
    cryptos = ['bitcoin', 'ethereum', 'polygon', 'solana', 'xrp']
    
    coins_price_list = [bitcoin_prices, ethereum_prices, polygon_prices, solana_prices, xrp_prices]

    return cryptos, exchanges, coins_price_list