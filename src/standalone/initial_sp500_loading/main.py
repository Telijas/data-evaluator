import csv
import os
from typing import List, Tuple

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "S&P_500_Historical_Components&Changes.csv")
old_sp500_set: set[str] = set({})
movements: List[Tuple[str, str, str]] = []
with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    # Iterate through rows
    for row in reader:
        if row[0] == 'date':
            continue
        date = row[0]
        raw_tickers = row[1].split(",")
        cleaned_tickers = set([item.split('-')[0] for item in raw_tickers])
        added_symbols = cleaned_tickers.difference(old_sp500_set)
        removed_symbols = old_sp500_set.difference(cleaned_tickers)
        old_sp500_set = cleaned_tickers
        movements.extend([(date, symbol, "ADDED") for symbol in added_symbols])
        movements.extend([(date, symbol, "REMOVED") for symbol in removed_symbols])

print("found movements: ", len(movements))
