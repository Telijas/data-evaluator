import csv
import os
from typing import List, Tuple

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "sp500_changes_since_2019.csv")
sql_statements: List[str] = []

with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) == 0 or row[0] == 'date':
            continue
        date = row[0]
        all_added = row[1].split(",")
        for added_ticker in all_added:
            if added_ticker != "":
                sql_statements.append(
                    f"INSERT INTO public.sp500_changes (symbol, business_date, \"action\") VALUES ('{added_ticker}', '{date}', 'ADDED') on conflict do nothing;")

        all_removed = row[2].split(",")
        for removed_ticker in all_removed:
            if removed_ticker != "":
                sql_statements.append(
                    f"INSERT INTO public.sp500_changes (symbol, business_date, \"action\") VALUES ('{removed_ticker}', '{date}', 'REMOVED') on conflict do nothing;")

# print(sql_statements)
for insert in sql_statements:
    print(insert)
