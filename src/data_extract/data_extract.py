from datetime import datetime, timedelta
import pandas as pd
import psycopg2


def extract_market_data(symbol: str, date: datetime, day_records_negative: int,
                        day_records_positive: int) -> pd.DataFrame:
    connection = psycopg2.connect(
        host="localhost",
        database="collector",
        user="postgres",
        password="password",
        port=6543
    )
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
    # print(df)
    return df


def get_SP500_entry_symbol_and_date() -> dict:
    result = {"CAT": datetime(1963, 2, 1),
              "AAPL": datetime(2024, 2, 1)
              }
    return result
