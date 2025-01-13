from datetime import datetime, timedelta
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt


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
    reference_value_stock_price = df.loc[reference_index, 'stock_price']
    df['stock_price_rel'] = (df['stock_price'] / reference_value_stock_price - 1) * 100
    reference_value_stock_traded = df.loc[reference_index, 'stock_traded']
    df['stock_traded_rel'] = (df['stock_traded'] / reference_value_stock_traded - 1) * 100
    # plt.figure(figsize=(8, 6))
    # plt.plot(df['offset'], df['stock_price_rel'], marker='o', linestyle='-', label=symbol)
    # plt.xlabel("Offset")
    # plt.ylabel("Relative Change")
    # plt.title("Relative Change vs Offset")
    # plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)  # Add a horizontal line at y=0
    # plt.grid(True)
    # plt.legend()

    # Show the plot
    # plt.show()
    # print(df)
    return df


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
