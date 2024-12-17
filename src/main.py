import pandas as pd
import psycopg2
import data_extract.data_extract as data_extract
from datetime import datetime


def main():
    data_extract.extract_market_data("CAT", datetime(1963, 2, 1), 10, 10)
    sp500_entries = data_extract.get_SP500_entry_symbol_and_date()
    stock_data = pd.DataFrame.empty
    # stock_data: pd.DataFrame
    for symbol, date in sp500_entries.items():
        if stock_data is pd.DataFrame.empty:
            stock_data = data_extract.extract_market_data(symbol, date, 10, 10)
        else:
            symbol_stock_data = data_extract.extract_market_data(symbol, date, 10, 10)
            stock_data = pd.concat([stock_data, symbol_stock_data])

    print(stock_data)
    print("done")


if __name__ == "__main__":
    main()
