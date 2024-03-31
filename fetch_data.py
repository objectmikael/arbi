"""Import libraries and/or dependencies.

CCXT: 
    - CryptoCurrency eXchange Trading is a Python library that provides a unified interface for 
    interacting with various cryptocurrency exchanges. It allows users to access market data, 
    execute trades, and manage accounts across multiple exchanges using a single, consistent API.   
"""
import ccxt

def fetch_data():
    """Get data from various exchanges for different cryptocurrencies.

    This function collects data for different cryptocurrencies from various exchanges
    using the ccxt library.

    Returns:
        tuple: A tuple containing:
            - List of cryptocurrency names
            - List of exchange names
            - List of lists containing prices for each cryptocurrency on each exchange
    """
    try:
        # Cryptocurrency names in alphabetical order
        cryptos = ['bitcoin', 'ethereum', 'polygon', 'solana', 'xrp']

        # Exchange names in alphabetical order
        exchanges = ['Binanceus', 'Bitstamp', 'Gemini', 'Kraken', 'Poloniex']

        # Initialize tickers per exchange 
        binance_tickers = ['BTCUSDT', 'ETHUSDT', 'MATICUSDT', 'SOLUSDT', 'XRPUSDT']
        bitstamp_tickers=['btcusd','ethusd','maticusd','solusd','xrpusd']
        kraken_tickers = ['XBTUSDT', 'ETHUSDT', 'MATICUSDT', 'SOLUSDT', 'XRPUSDT']
        gemini_tickers=['btcusd','ethusd','maticusd','solusd','xrpusd']
        poloniex_tickers = ['BTC_USDT', 'ETH_USDT', 'MATIC_USDT', 'SOL_USDT', 'XRP_USDT']

        tickers_per_exchange = [binance_tickers, bitstamp_tickers, gemini_tickers, kraken_tickers,  poloniex_tickers]

        exchange_prices = [[] for _ in range(len(exchanges))]

        for i, exchange_name in enumerate(exchanges):
            exchange = getattr(ccxt, exchange_name.lower())()
            for j, ticker in enumerate(tickers_per_exchange[i]):
                try:
                    ticker_data = exchange.fetch_ticker(ticker)
                    ask_price = float(ticker_data['ask'])
                    bid_price = float(ticker_data['bid'])
                    exchange_prices[i].append([ask_price, bid_price])
                except (ccxt.NetworkError, ccxt.BaseError) as e:
                    print(f'Error occured while fetching data from {exchange_name} for {cryptos[j]}: {e}')
                    exchange_prices[i].append([None, None])

        # Transpose exchange_prices to get coins_list
        coins_price_list = list(map(list, zip(*exchange_prices)))

        return cryptos, exchanges, coins_price_list
    
    except Exception as e:
        print(f'An unexpected error occured: {e}')
        return None, None, None
    

fetch_data()