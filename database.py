"""Databse Specific Instructions 

Follow the docstring(s) below.
"""
import os
from dotenv import load_dotenv
from sqlalchemy.inspection import inspect
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String
from sqlalchemy.exc import OperationalError, IntegrityError, DataError

def create_table():
    """Create a table in a PostgreSQL database. 
    This function creates a table named 'trades' in a PostgreSQL database 
    using the provided environment variables for database connection details.

    Returns:
        A tuple containing the SQlAlchemy Table object representing the created table 
        and the SQLAlchemy Engine object representing the database connection. 
    """
    try:
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

    except (OperationalError, IntegrityError, DataError) as e:
        print(f'The following error occured in the database script: {e}')