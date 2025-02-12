import pandas as pd
import psycopg2
import data_extract.data_extract as data_extract
import evaluation.preprocessing as preprocessing
import data_quality.sp500_stock_quality as sp500_stock_quality
from datetime import datetime
import matplotlib.pyplot as plt

date_range = 30


def main():
    do_show_analysis()


def do_show_analysis():
    # data_extract.extract_market_data("CAT", datetime(1963, 2, 1), 10, 10)
    sp500_entries = data_extract.get_SP500_entry_symbol_and_date()
    stock_data = pd.DataFrame.empty
    # stock_data: pd.DataFrame
    for symbol, date in sp500_entries.items():
        if stock_data is pd.DataFrame.empty:
            stock_data = data_extract.extract_market_data(symbol, date, date_range, date_range)
        else:
            symbol_stock_data = data_extract.extract_market_data(symbol, date, date_range, date_range)
            stock_data = pd.concat([stock_data, symbol_stock_data])

    # Group by symbol
    grouped = stock_data.groupby('symbol')
    for symbol, group in grouped:
        plt.plot(group['offset'], group['stock_price_rel'], linestyle='-', label=symbol)
    plt.xlabel("Offset")
    plt.ylabel("Relative Change")
    plt.title("Relative Change vs Offset for Multiple Symbols")
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)  # Add a horizontal line at y=0
    plt.grid(True)
    plt.legend()
    plt.show()

    for symbol, group in grouped:
        plt.plot(group['offset'], group['stock_traded_rel'], linestyle='-', label=symbol)
    plt.xlabel("Offset")
    plt.ylabel("Relative Change")
    plt.title("Relative Change vs Offset for Multiple Symbols")
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)  # Add a horizontal line at y=0
    plt.grid(True)
    plt.legend()
    plt.show()

    print("done")


# if __name__ == "__main__":
#     main()

if __name__ == "__main__":
    # sp500_list = data_extract.get_market_data(['ACN', 'ABC', 'ACV', 'AAPL'], datetime(2024, 11, 1))
    # sp500_list = preprocessing.filter_symbols_by_market_capitalization(sp500_list)
    # print(sp500_list.to_string())
    sp500_stock_quality.display_sp500_quality_of_year(2024)
