from datetime import datetime

import pandas as pd

import src.data_extract.data_extract as data_extract

market_capitalization_lower_limit = 12700000000
monthly_shares_traded_lower_limit = 2500000


def get_sp500_master_data_candidate(date: datetime) -> list[str]:
    candidates = data_extract.get_master_data_eligible_symbols()
    candidates = list(set(candidates) - set(data_extract.get_current_sp500_list(date)))
    return candidates


def filter_symbols_by_market_capitalization(df: pd.DataFrame) -> pd.DataFrame:
    df['market_cap_reached'] = df['min_market_capitalization'].ge(market_capitalization_lower_limit)
    filtered_symbols = df.groupby("symbol").filter(lambda x: x["market_cap_reached"].all())
    filtered_symbols.drop(columns=["market_cap_reached"], inplace=True)
    filtered_symbols = filtered_symbols.reset_index(drop=True)
    return filtered_symbols


def filter_symbols_by_stock_traded(df: pd.DataFrame) -> pd.DataFrame:
    df['stock_traded_cap_reached'] = df['total_stock_traded'].ge(monthly_shares_traded_lower_limit)
    filtered_symbols = df.groupby("symbol").filter(lambda x: x["stock_traded_cap_reached"].all())
    filtered_symbols.drop(columns=["stock_traded_cap_reached"], inplace=True)
    filtered_symbols = filtered_symbols.reset_index(drop=True)
    return filtered_symbols
