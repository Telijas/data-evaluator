import datetime

from matplotlib import pyplot as plt

import src.data_extract.data_extract as data_extract


def display_sp500_quality_of_year(year: int):
    print(f"Start quality check for year {year}.")
    date = datetime.datetime(year=year, month=12, day=31)
    sp500_stock = data_extract.get_current_sp500_list(date)
    sp500_market_data = data_extract.get_market_data(sp500_stock, date, 11)
    symbols_in_data = sp500_market_data["symbol"].nunique()

    ## Display basic data availability
    print(f"Symbols found in SP500 list: {len(sp500_stock)}\n"
          f"Out of them in market data: {symbols_in_data}\n"
          f"Coverage: {symbols_in_data / len(sp500_stock)}\n")

    ## Show if data for all year month exist
    print(f"Expected amount of rows: {len(sp500_stock) * 12}\n"
          f"Found year month combinations: {len(sp500_market_data)}\n"
          f"Coverage: {len(sp500_market_data) / (len(sp500_stock) * 12):.4f}.\n")

    ## Show coverage of time series elements
    missing_total_order_amount = sp500_market_data["total_order_amount"].isna().sum()
    missing_total_stock_traded = sp500_market_data["total_stock_traded"].isna().sum()
    missing_min_market_capitalization = sp500_market_data["min_market_capitalization"].isna().sum()
    print(f"Expected amount of time series elements rows: {len(sp500_stock) * 12}\n"
          f"Found coverage for total_order_amount: {(len(sp500_market_data) - missing_total_order_amount) / (len(sp500_stock) * 12):.4f}\n"
          f"Found coverage for total_stock_traded: {(len(sp500_market_data) - missing_total_stock_traded) / (len(sp500_stock) * 12):.4f}\n"
          f"Found coverage for min_market_capitalization: {(len(sp500_market_data) - missing_min_market_capitalization) / (len(sp500_stock) * 12):.4f}")

    ## Group show available data
    sp500_market_data = sp500_market_data.groupby("year_month")[
        ["total_order_amount", "total_stock_traded", "min_market_capitalization"]].apply(
        lambda x: (len(sp500_stock) - x.isna().sum()) / len(sp500_stock)).reset_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(sp500_market_data["year_month"], sp500_market_data["total_order_amount"], marker='o', linestyle='-',
            label="total_order_amount")
    ax.plot(sp500_market_data["year_month"], sp500_market_data["total_stock_traded"], marker='s', linestyle='--',
            label="total_stock_traded")
    ax.plot(sp500_market_data["year_month"], sp500_market_data["min_market_capitalization"], marker='o', linestyle='-',
            label="min_market_capitalization")
    ax.set_title(f"Data availability of SP500 for year {year}")
    ax.set_xlabel("Year month")
    ax.set_ylabel("Coverage existing data")
    ax.set_ylim(0, 1)
    ax.grid(True)
    ax.legend()
    plt.show()
    return None
