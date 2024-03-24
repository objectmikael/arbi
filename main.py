"""Main Script Specific Instructions 

Follow the docstring(s) below.
"""
import time
from datetime import datetime
from database import create_table
from fetch_data import fetch_data

# Global Variables
wallet = 3000 #provide a dollar amount you wish to invest. Value should be an interger/float. 
fund_allocation = [0.2, 0.2, 0.3, .15, 0.15] # provide your wallet allocation in a list in the following order [bitcoin, ethereum, polygon, solana, xrp]. Summation of allocation values should equal 1. 
min_profit_threshold = 0 # provide a minimum profit threshold. This value will manage the size of returns you're intrested in. Value should be less than 1.   

# Define arbitrage function
def find_arbitrage(exchange_a, exchange_b):
    """ Add docstring details here
    """
    try:
        ask_price_a = exchange_a[0]
        bid_price_b = exchange_b[1]

        spread_percent = ((bid_price_b - ask_price_a) / ask_price_a * 100)

        return spread_percent, ask_price_a, bid_price_b
    except Exception as e:
        print(f'The following error occured in the arbitrage function: {e}')

# Define main function
def main():
    """ Add docstring details here
    """
    try:
        # Initialize the trades and engine variable from create_table function
        trades, engine = create_table()

        # Access prices from APIs
        cryptos, exchanges, coins_price_list = fetch_data()

        # Set the current time
        current_datetime = datetime.now().isoformat()

        ## Variables
        global wallet
        global fund_allocation
        global min_profit_threshold
        profits = 0
        spent_total = 0
        max_spread = 0
        max_spread_combination = None

        bitcoin_wallet = wallet*fund_allocation[0]
        ethereum_wallet = wallet*fund_allocation[1]
        polygon_wallet = wallet*fund_allocation[2]
        solana_wallet = wallet*fund_allocation[3]
        xrp_wallet = wallet*fund_allocation[4]

        wallet_list = [bitcoin_wallet, ethereum_wallet, polygon_wallet, solana_wallet, xrp_wallet]

        # Execute Trades
        for i, coin_list in enumerate(coins_price_list):
            for j, _ in enumerate(coin_list):
                for k, _ in enumerate(coin_list):
                    if j != k:
                        exchange_a, exchange_b = coin_list[j], coin_list[k]
                        exchange_name_a, exchange_name_b = exchanges[j], exchanges[k]

                        spread_percentage, buy_price, sell_price = find_arbitrage(exchange_a, exchange_b)

                        if spread_percentage > max_spread:
                            max_spread = spread_percentage
                            max_spread_combination = [spread_percentage, buy_price, sell_price, exchange_name_a, exchange_name_b]

            if max_spread_combination[0] > min_profit_threshold:
                shares = wallet_list[i] / max_spread_combination[1]
                purchase_price = shares*max_spread_combination[1]
                sale_price = shares*max_spread_combination[2]
                profit = sale_price - purchase_price
                profits += profit
                wallet_list[i] -= purchase_price
                wallet -= purchase_price
                spent_total += purchase_price

                insert_row = trades.insert().values(
                    current_datetime = current_datetime,
                    currency = cryptos[i],
                    volume = shares,
                    buy_exchange = max_spread_combination[3],
                    buy_price = max_spread_combination[1],
                    total_purchase_amount = purchase_price,
                    sell_exchange = max_spread_combination[4],
                    sell_price = max_spread_combination[2],
                    total_sale_amount = sale_price,
                    profit = profit,
                    spread_percentage = max_spread_combination[0],
                    wallet_balance = wallet
                )

                with engine.connect() as connection:
                    connection.execute(insert_row)
            
            max_spread = 0
            max_spread_combination = None

        wallet = spent_total + wallet + profits
        print('Trading in progress...')
    except Exception as e:
        print(f'The following error occured in the main function: {e}')

# Define a function to loop the main function
def main_loop():
    """ Add docstring details here
    """
    global wallet
    try:
        while True:
            main()
            time.sleep(30)
    except KeyboardInterrupt:
        print("Program terminated by user.")

# Call function to run all code above
main_loop()