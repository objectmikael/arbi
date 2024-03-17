import os
from dotenv import load_dotenv
from sqlalchemy.inspection import inspect
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String

def create_table():
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

    trades = Table(
        'trades',
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
        Column('spread_percentage', Float),
        Column('wallet_balance', Float),
    )

    # Execute the table creation
    # Check if the table exist before creating
    if not inspect(engine).has_table('trades'):
        metadata.create_all(engine)

    return trades, engine