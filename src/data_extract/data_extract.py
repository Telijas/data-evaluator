from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

host = "localhost"
database = "collector"
user = "postgres"
password = "password"
port = 6543


def extract_market_data(symbol: str, date: datetime, day_records_negative: int,
                        day_records_positive: int) -> pd.DataFrame:
    connection = _get_connection()
    upper_date = (date + timedelta(int(day_records_positive * (7 / 5) + 10))).strftime('%Y-%m-%d')
    lower_date = (date - timedelta(int(day_records_negative * (7 / 5) + 10))).strftime('%Y-%m-%d')
    query = f"SELECT * FROM market_data where '{lower_date}' <= business_date and  business_date <= '{upper_date}' and symbol = '{symbol}' order by business_date"
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=columns)
    connection.close()

    df['business_date'] = pd.to_datetime(df['business_date'])
    reference_index = df[df['business_date'] == date].index[0]
    df['offset'] = df.index - reference_index
    df = df[(-1) * day_records_negative <= df['offset']]
    df = df[df['offset'] <= day_records_positive]
    reference_value_stock_price = df.loc[reference_index, 'stock_price']
    df['stock_price_rel'] = (df['stock_price'] / reference_value_stock_price - 1) * 100
    reference_value_stock_traded = df.loc[reference_index, 'stock_traded']
    df['stock_traded_rel'] = (df['stock_traded'] / reference_value_stock_traded - 1) * 100
    return df


def _get_connection():
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )
    return connection


def get_SP500_entry_symbol_and_date() -> dict:
    result = {"TPL": datetime(2024, 11, 26),
              "AMTM": datetime(2024, 9, 30),
              "ERIE": datetime(2024, 9, 23),
              "DELL": datetime(2024, 9, 23),
              "PLTR": datetime(2024, 9, 23),
              "SW": datetime(2024, 7, 8),
              "GDDY": datetime(2024, 6, 24),
              "CRWD": datetime(2024, 6, 24),
              "KKR": datetime(2024, 6, 24),
              "VST": datetime(2024, 5, 8),
              "SOLV": datetime(2024, 4, 3),
              "GEV": datetime(2024, 4, 3)
              }
    return result


def get_current_sp500_list(date: datetime) -> list[str]:
    """
    Get the current list of SP500 symbols, by giving a date.
    :param date: Date of validity for the SP500 list
    :return: List of symbols (string)
    """
    connection = _get_connection()
    query = f"select symbol from  sp500('{date}') order by symbol"
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.close()
    return [str(tup[0]) for tup in rows]


def get_most_recent_sp500_entering_date(symbol: str) -> Optional[datetime]:
    connection = _get_connection()
    query = f"select max(sc.business_date) as business_date from sp500_changes sc where symbol = '{symbol}' and sc.\"action\" = 'ADDED';"
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.close()
    if len(rows) == 0:
        return None
    return rows[0][0]


def get_master_data_eligible_symbols() -> list[str]:
    connection = _get_connection()
    query = "select issue_symbol as symbol from master_data_eligible"
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.close()
    return [str(tup[0]) for tup in rows]


def get_market_data(symbols: list[str], end_date: datetime, past_month_included=6) -> pd.DataFrame:
    connection = _get_connection()
    formatted_symbols = ", ".join(f"'{item}'" for item in symbols)
    # date_string =
    query = f"SELECT      symbol,     year_month,     SUM(order_amount) AS total_order_amount,     SUM(stock_traded) AS total_stock_traded,     MIN(market_capitalization) as min_market_capitalization FROM public.market_data WHERE year_month >= (     EXTRACT(YEAR FROM DATE '{end_date}' - INTERVAL '{past_month_included} months') * 100 +       EXTRACT(MONTH FROM DATE '{end_date}' - INTERVAL '{past_month_included} months') ) and year_month <= (     EXTRACT(YEAR FROM DATE '{end_date}') * 100 +  EXTRACT(MONTH FROM DATE '{end_date}' ) ) and symbol in ({formatted_symbols}) GROUP BY symbol, year_month ORDER BY symbol, year_month;"
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.close()

    column_names = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=column_names)
    df['year_month'] = pd.to_datetime(df['year_month'].astype(str), format='%Y%m')
    return df
