"""Cryptocurrency Arbitrage Bot

This script implements a cryptocurrency arbitrage bot that identifies arbitrage opportunities
across different exchanges and executes trades based on predefined criteria.
"""
import time
from datetime import datetime
from database import create_table
from fetch_data import fetch_data

# Global Variables
wallet = 3000 # Dollar amount to invest.
fund_allocation = [0.2, 0.2, 0.3, .15, 0.15] # Allocation of funds for each cryptocurrency [bitcoin, ethereum, polygon, solana, xrp].
min_profit_threshold = 0.25 # Minimum profit threshold.

# Define arbitrage function
def find_arbitrage(exchange_a, exchange_b):
    """
    Find arbitrage opportunity between two exchanges.

    Args:
        exchange_a (list): Ask and bid prices for exchange A.
        exchange_b (list): Ask and bid prices for exchange B.

    Returns:
        tuple: Arbitrage spread percentage, ask price of exchange A, bid price of exchange B.
    """
    try:
        if None not in exchange_a and None not in exchange_b:
            ask_price_a = exchange_a[0]
            bid_price_b = exchange_b[1]

            spread_percent = ((bid_price_b - ask_price_a) / ask_price_a * 100)

            return spread_percent, ask_price_a, bid_price_b
    except Exception as e:
        print(f'The following error occured in the arbitrage function: {e}')
        return None, None, None

# Define main function
def main():
    """Main function to execute cryptocurrency arbitrage.
    """
    try:
        # Initialize database table
        trades, engine = create_table()

        # Get cryptocurrency data from exchanges
        cryptos, exchanges, coins_price_list = fetch_data()

        # Set current datetime
        current_datetime = datetime.now().isoformat()

        ## Variables
        global wallet 
        global fund_allocation
        global min_profit_threshold
        profits = 0
        spent_total = 0
        max_spread = 0
        max_spread_combination = None

        # Calculate wallet allocation
        wallet_list = [wallet * allocation for allocation in fund_allocation]

        # Execute Trades
        for i, coin_list in enumerate(coins_price_list):
            for j, _ in enumerate(coin_list):
                for k, _ in enumerate(coin_list):
                    if j != k:
                        exchange_a, exchange_b = coin_list[j], coin_list[k]
                        if None not in exchange_a and None not in exchange_b:
                            exchange_name_a, exchange_name_b = exchanges[j], exchanges[k]
                            spread_percentage, buy_price, sell_price = find_arbitrage(exchange_a, exchange_b)
                            
                            if spread_percentage is not None and spread_percentage > max_spread:
                                max_spread = spread_percentage
                                max_spread_combination = [spread_percentage, buy_price, sell_price, exchange_name_a, exchange_name_b]
            
            if max_spread_combination[0] > min_profit_threshold:
                shares = wallet_list[i] / max_spread_combination[1]
                purchase_price = shares*max_spread_combination[1]
                sale_price = shares*max_spread_combination[2]

                # Calculate profit
                profit = sale_price - purchase_price
                profits += profit
                wallet_list[i] -= purchase_price
                wallet -= purchase_price
                spent_total += purchase_price
                
                # Insert trade record into database
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
        print(f'An error occured: {e}')


# Define function to continuously run the main function
def main_loop():
    """Function to continuously run the main function.
    """
    global wallet
    try:
        while True:
            main()
            time.sleep(5)
    except KeyboardInterrupt:
        print("Program terminated by user.")

# Call function to run all code above
main_loop()